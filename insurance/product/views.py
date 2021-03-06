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

from .view_mixins import CompanyLoginRequiredMixin

from .serializers import product_response_serialize

from users.models import Company, User, Worker
from search.forms import SearchFilterForm

from .tasks import send_mail_on_response_product
from .redis import (
    get_and_incr_view_count_product_option,
    get_view_count_product_option_from_list,
)


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


class ProductCategoryCreateView(CompanyLoginRequiredMixin, CreateView):
    model = ProductCategory
    context_object_name = "product_category"
    template_name = "product_category/view.html"
    form_class = ProductCategoryForm
    success_url = reverse_lazy("lk_home")


class ProductCreateView(CompanyLoginRequiredMixin, CreateView):
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


class ProductUpdateView(CompanyLoginRequiredMixin, UpdateView):
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


class ProductDeleteView(CompanyLoginRequiredMixin, DeleteView):
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

            # ???????????????? ?????????????????????? ???? ?????????? ???????????????? ?? ?????????? ??????????????
            data = product_response_serialize(product_response)
            url_product = request.build_absolute_uri(
                reverse(
                    "product_option_detail",
                    kwargs={"pk": product_response.product_option.pk},
                )
            )
            data["url_product"] = url_product

            send_mail_on_response_product.apply_async(
                (data,),
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


class ProductOptionCreateView(CompanyLoginRequiredMixin, CreateView):
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


class ProductOptionUpdateView(CompanyLoginRequiredMixin, UpdateView):
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


class ProductOptionDeleteView(CompanyLoginRequiredMixin, DeleteView):
    model = ProductOption
    success_url = reverse_lazy("lk_home")

    def get(self, request, *args, **kwargs):
        if self.validate_product_option():
            return super().post(request, *args, **kwargs)
        return redirect(
            reverse_lazy("product_option_detail", kwargs={"pk": self.kwargs.get("pk")})
        )


class CabinetView(CompanyLoginRequiredMixin, TemplateView):
    template_name = "lk/home.html"

    def get_context_data(self, **kwargs):
        products = Product.objects.filter(
            company__worker__user=self.request.user
        ).order_by("id")
        kwargs["products"] = products

        product_option_pks = ProductOption.objects.filter(
            product__company__worker__user=self.request.user
        ).values_list("pk", flat=True)
        view_counts = get_view_count_product_option_from_list(product_option_pks)
        kwargs["view_counts"] = {
            key.split("_")[-1]: value for key, value in view_counts.items()
        }

        return super().get_context_data(**kwargs)


class ResponseSuccessView(DeleteView):
    model = ProductResponse
    context_object_name = "product_response"
    template_name = "product_response/success.html"


class ProductResponseView(CompanyLoginRequiredMixin, TemplateView):
    template_name = "product_response/all_responses.html"

    def get_context_data(self, **kwargs):
        if self.user_is_worker():
            product_responses = ProductResponse.objects.filter(
                product_option__product__company__worker__user=self.request.user
            ).order_by("-id")
            kwargs["product_responses"] = product_responses
        return super().get_context_data(**kwargs)
