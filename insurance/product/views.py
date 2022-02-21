from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, UpdateView, TemplateView
from django.views.generic.edit import DeleteView, CreateView
from django.urls import reverse_lazy, reverse
from .models import ProductOption, Product, ProductCategory, ProductResponse
from .forms import (
    ProductOptionForm,
    ProductForm,
    ProductCategoryForm,
    ProductResponseForm,
    CompanyForm,
)

from users.models import Company, User, Worker
from search.forms import SearchFilterForm

from .tasks import send_mail_on_response_product
from .redis import (
    get_and_incr_view_count_product_option,
    get_all_view_count_product_option,
)


class ValidateAuthCompany(LoginRequiredMixin):
    def auth_is_company(self) -> bool:
        """Проверка, что пользователь авторизовался как компания."""
        # return isinstance(self.request.user, Company)
        return Worker.objects.filter(user=self.request.user).exists()

    def validate_product(self) -> bool:
        """
        Проверка, что авторизованный пользователь(компания) владелец продукта.
        """

        if self.auth_is_company():

            is_owner_product = Product.objects.filter(
                pk=self.kwargs.get("pk"), company=self.request.user.worker.company
            ).exists()

            return is_owner_product
        return False

    def validate_product_option(self) -> bool:
        """
        Проверка, что авторизованный пользователь(компания) относится к конфигурации продукта.
        """

        if self.auth_is_company():
            is_owner_product = ProductOption.objects.filter(
                pk=self.kwargs.get("pk"),
                product__company=self.request.user.worker.company,
            ).exists()

            return is_owner_product
        return False


class CompanyCreateView(CreateView):
    model = Company
    context_object_name = "company"
    template_name = "company/view.html"
    form_class = CompanyForm

    def form_valid(self, form):
        self.object = form.save()
        worker = Worker(user=self.request.user, company=self.object, is_owner=True)
        worker.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("home")


class ProductCategoryCreateView(ValidateAuthCompany, CreateView):
    model = ProductCategory
    context_object_name = "product_category"
    template_name = "product_category/view.html"
    form_class = ProductCategoryForm
    success_url = reverse_lazy("lk_home")


class ProductCreateView(ValidateAuthCompany, CreateView):
    model = Product
    context_object_name = "product"
    template_name = "product/view.html"
    form_class = ProductForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.company = self.request.user.worker.company
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("product_detail", kwargs={"pk": self.object.id})


class ProductDetailView(DetailView):
    model = Product
    context_object_name = "product"
    template_name = "product/view.html"


class ProductUpdateView(ValidateAuthCompany, UpdateView):
    model = Product
    context_object_name = "product"
    template_name = "product/view.html"
    form_class = ProductForm

    def get(self, request, *args, **kwargs):
        if self.validate_product():
            return super().get(request, *args, **kwargs)
        return redirect(
            reverse_lazy("product_detail", kwargs={"pk": self.kwargs.get("pk")})
        )

    def get_success_url(self):
        return reverse_lazy("product_detail", kwargs={"pk": self.kwargs.get("pk")})


class ProductDeleteView(ValidateAuthCompany, DeleteView):
    model = Product
    success_url = reverse_lazy("lk_home")

    def get(self, request, *args, **kwargs):
        if self.validate_product():
            return super().post(request, *args, **kwargs)
        return redirect(
            reverse_lazy("product_detail", kwargs={"pk": self.kwargs.get("pk")})
        )


class ProductOptionView(ListView):
    model = ProductOption
    template_name = "product_option/index.html"

    def get_context_data(self, **kwargs):
        kwargs["filter_form"] = SearchFilterForm
        return super().get_context_data(**kwargs)


class ProductOptionDetailView(DetailView):
    model = ProductOption
    context_object_name = "product_option"
    template_name = "product_option/view.html"

    def get_context_data(self, **kwargs):
        form_response = ProductResponseForm()
        kwargs["form_response"] = form_response
        kwargs["view_count"] = get_and_incr_view_count_product_option(
            pk=self.kwargs["pk"]
        )
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        form_response = ProductResponseForm(request.POST)
        if form_response.is_valid():
            product_response = form_response.save(commit=False)
            product_response.product_option = self.model.objects.get(
                pk=self.kwargs["pk"]
            )
            product_response.save()

            # отправка уведомления на почту компании о новом отклике
            to = product_response.product_option.product.company.email
            fullname = product_response.full_name
            phone = product_response.phone
            email = product_response.email
            url_product = request.build_absolute_uri(
                reverse(
                    "product_option_detail",
                    kwargs={"pk": product_response.product_option.pk},
                )
            )

            send_mail_on_response_product.apply_async(
                (fullname, phone, email, url_product, to),
                retry=True,
                retry_policy={
                    "max_retries": 5,
                    "interval_start": 1,
                    "interval_step": 5,
                    "interval_max": 15,
                },
            )

            return redirect(
                reverse_lazy(
                    "product_response_success", kwargs={"pk": product_response.pk}
                )
            )
        return redirect(
            reverse_lazy("product_option_detail", kwargs={"pk": self.kwargs.get("pk")})
        )


class ProductOptionCreateView(ValidateAuthCompany, CreateView):
    model = ProductOption
    context_object_name = "product_option"
    template_name = "product_option/view.html"
    form_class = ProductOptionForm

    def get_form(self, *args, **kwargs):
        products_current_company = Product.objects.filter(
            company=self.request.user.worker.company
        )

        form = super().get_form(*args, **kwargs)
        form.fields["product"].choices = (
            (product.pk, product.__str__) for product in products_current_company
        )
        return form

    def get_success_url(self):
        return reverse_lazy("product_option_detail", kwargs={"pk": self.object.id})


class ProductOptionUpdateView(ValidateAuthCompany, UpdateView):
    model = ProductOption
    context_object_name = "product_option"
    template_name = "product_option/view.html"
    form_class = ProductOptionForm

    def get(self, request, *args, **kwargs):
        if self.validate_product_option():
            return super().get(request, *args, **kwargs)
        return redirect(
            reverse_lazy("product_option_detail", kwargs={"pk": self.kwargs.get("pk")})
        )

    def get_form(self, *args, **kwargs):
        products_current_company = Product.objects.filter(
            company=self.request.user.worker.company
        )

        form = super().get_form(*args, **kwargs)
        form.fields["product"].choices = (
            (product.pk, product.__str__) for product in products_current_company
        )
        return form

    def get_success_url(self):
        return reverse_lazy(
            "product_option_detail", kwargs={"pk": self.kwargs.get("pk")}
        )


class ProductOptionDeleteView(ValidateAuthCompany, DeleteView):
    model = ProductOption
    success_url = reverse_lazy("lk_home")

    def get(self, request, *args, **kwargs):
        if self.validate_product_option():
            return super().post(request, *args, **kwargs)
        return redirect(
            reverse_lazy("product_option_detail", kwargs={"pk": self.kwargs.get("pk")})
        )


class CabinetView(ValidateAuthCompany, TemplateView):
    template_name = "lk/home.html"

    def get_context_data(self, **kwargs):
        products = Product.objects.filter(
            company=self.request.user.worker.company
        ).order_by("id")
        kwargs["products"] = products

        view_counts = get_all_view_count_product_option()
        kwargs["view_counts"] = {
            key.split("_")[-1]: value for key, value in view_counts.items()
        }

        return super().get_context_data(**kwargs)


class ResponseSuccessView(DeleteView):
    model = ProductResponse
    context_object_name = "product_response"
    template_name = "product_response/success.html"


class ProductResponseView(ValidateAuthCompany, TemplateView):
    template_name = "product_response/all_responses.html"

    def get_context_data(self, **kwargs):
        if self.auth_is_company():
            product_responses = ProductResponse.objects.filter(
                product_option__product__company=self.request.user.worker.company
            ).order_by("-id")
            kwargs["product_responses"] = product_responses
        return super().get_context_data(**kwargs)
