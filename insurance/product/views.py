from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, UpdateView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from .models import ProductOption, Product
from .forms import ProductOptionForm


class ValidateAuthCompany(LoginRequiredMixin):
    def validate_product_option(self):
        """
        Проверка, что авторизованный пользователь(компания) относится к конфигурации продукта.
        """
        is_current_company = ProductOption.objects.filter(
            pk=self.kwargs.get("pk"), product__company=self.request.user
        ).exists()

        return is_current_company


class ProductOptionView(ListView):
    model = ProductOption
    template_name = "product/index.html"


class ProductOptionDetailView(DetailView):
    model = ProductOption
    context_object_name = "product_option"
    template_name = "product/view.html"


class ProductOptionUpdateView(ValidateAuthCompany, UpdateView):
    model = ProductOption
    context_object_name = "product_option"
    template_name = "product/view.html"
    form_class = ProductOptionForm

    def get(self, request, *args, **kwargs):
        if self.validate_product_option():
            return super().get(request, *args, **kwargs)
        return redirect(
            reverse_lazy("product_detail", kwargs={"pk": self.kwargs.get("pk")})
        )

    def get_form(self, *args, **kwargs):
        products_current_company = Product.objects.filter(company=self.request.user)

        form = super().get_form(*args, **kwargs)
        form.fields["product"].choices = (
            (product.pk, product.__str__) for product in products_current_company
        )
        return form

    def get_success_url(self):
        return reverse_lazy("product_detail", kwargs={"pk": self.kwargs.get("pk")})


class ProductOptionDeleteView(ValidateAuthCompany, DeleteView):
    model = ProductOption
    success_url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        if self.validate_product_option():
            return super().post(request, *args, **kwargs)
        return redirect(
            reverse_lazy("product_detail", kwargs={"pk": self.kwargs.get("pk")})
        )
