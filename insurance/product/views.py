from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, UpdateView, TemplateView
from django.views.generic.edit import DeleteView, CreateView
from django.urls import reverse_lazy
from .models import ProductOption, Product, ProductCategory, ProductResponse
from .forms import ProductOptionForm, ProductForm, ProductCategoryForm, ProductResponseForm
from users.models import Company


class ValidateAuthCompany(LoginRequiredMixin):
    def auth_is_company(self) -> bool:
        """Проверка, что пользователь авторизовался как компания."""
        return isinstance(self.request.user, Company)

    def validate_product(self) -> bool:
        """
        Проверка, что авторизованный пользователь(компания) владелец продукта.
        """

        if self.auth_is_company():

            is_owner_product = Product.objects.filter(
                pk=self.kwargs.get("pk"), company=self.request.user
            ).exists()

            return is_owner_product
        return False

    def validate_product_option(self) -> bool:
        """
        Проверка, что авторизованный пользователь(компания) относится к конфигурации продукта.
        """

        if self.auth_is_company():

            is_owner_product = ProductOption.objects.filter(
                pk=self.kwargs.get("pk"), product__company=self.request.user
            ).exists()

            return is_owner_product
        return False


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
        self.object.company = self.request.user
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


class ProductOptionDetailView(DetailView):
    model = ProductOption
    context_object_name = "product_option"
    template_name = "product_option/view.html"

    def get_context_data(self, **kwargs):
        form_response = ProductResponseForm()
        kwargs["form_response"] = form_response
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        form_response = ProductResponseForm(request.POST)
        if form_response.is_valid():
            product_response = form_response.save(commit=False)
            product_response.product_option = self.model.objects.get(pk=self.kwargs["pk"])
            product_response.save()
            return redirect(
                reverse_lazy("product_response_success", kwargs={"pk": product_response.pk})
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
        products_current_company = Product.objects.filter(company=self.request.user)

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
        products_current_company = Product.objects.filter(company=self.request.user)

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
        products = Product.objects.filter(company=self.request.user).order_by("id")
        kwargs["products"] = products
        return super().get_context_data(**kwargs)


class ResponseSuccessView(DeleteView):
    model = ProductResponse
    context_object_name = "product_response"
    template_name = "product_response/success.html"


class ProductResponseView(ValidateAuthCompany, TemplateView):
    template_name = "product_response/all_responses.html"

    def get_context_data(self, **kwargs):
        product_responses = ProductResponse.objects.filter(product_option__product__company=self.request.user)
        kwargs["product_responses"] = product_responses
        return super().get_context_data(**kwargs)

