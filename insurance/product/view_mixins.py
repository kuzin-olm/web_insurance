from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect

from .models import ProductOption, Product
from users.models import Company, User, Worker


class CompanyLoginRequiredMixin(LoginRequiredMixin):
    def user_is_worker(self) -> bool:
        """Проверка, что пользователь работает в какой-либо компании."""
        return Worker.objects.filter(user=self.request.user).exists()

    def validate_product(self) -> bool:
        """
        Проверка, что пользователь - сотрудник компании-владелеца продукта.
        """

        if self.user_is_worker():

            is_owner_product = Product.objects.filter(
                pk=self.kwargs.get("pk"), company=self.request.user.worker.company
            ).exists()

            return is_owner_product
        return False

    def validate_product_option(self) -> bool:
        """
        Проверка, что пользователь - сотрудник компании-владелеца конфигурации продукта.
        """

        if self.user_is_worker():
            is_owner_product = ProductOption.objects.filter(
                pk=self.kwargs.get("pk"),
                product__company=self.request.user.worker.company,
            ).exists()

            return is_owner_product
        return False

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not self.user_is_worker():
            messages.warning(request, "Вы не являетесь работником компании.")
            return redirect(request.META.get('HTTP_REFERER', '/'))
        return super().dispatch(request, *args, **kwargs)
