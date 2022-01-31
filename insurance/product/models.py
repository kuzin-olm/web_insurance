from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

from users.models import Company


class ProductCategory(models.Model):
    class Meta:
        verbose_name = "Категория продукта"
        verbose_name_plural = "Категории продуктов"

    name = models.CharField(
        max_length=255, verbose_name="Название", blank=False, unique=True
    )

    def __str__(self):
        return f"<Категория: {self.name}>"


class Product(models.Model):
    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    category = models.ForeignKey(
        to=ProductCategory, on_delete=models.CASCADE, verbose_name="категория"
    )
    company = models.ForeignKey(
        to=Company, on_delete=models.CASCADE, verbose_name="компания"
    )
    name = models.CharField(max_length=255, verbose_name="название продукта")
    description = models.TextField(blank=True, verbose_name="описание")
    is_active = models.BooleanField(default=False, verbose_name="продукт актуален")

    def __str__(self):
        return f"<Продукт: {self.name} категории: {self.category.name}>"


class ProductOption(models.Model):
    class Meta:
        verbose_name = "Конфигурация продукта"
        verbose_name_plural = "Конфигурации продуктов"

    product = models.ForeignKey(
        to=Product, verbose_name="продукт", on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="цена")
    expire = models.IntegerField(verbose_name="срок предоставления услуги")
    rate = models.DecimalField(
        max_digits=3, decimal_places=2, verbose_name="ставка в процентах"
    )
    date = models.DateTimeField(verbose_name="дата публикации", default=timezone.now)
    is_active = models.BooleanField(default=False, verbose_name="услуга активна")

    def __str__(self):
        return f"<Конфигурация продукта: {self.product.name}>"


class ProductResponse(models.Model):
    class Meta:
        verbose_name = "отклик на продукт"
        verbose_name_plural = "отклики на продукты"

    product_option = models.ForeignKey(
        to=ProductOption, on_delete=models.CASCADE, verbose_name="интересующий продукт"
    )

    full_name = models.CharField(max_length=255, verbose_name="Ф.И.О")
    email = models.EmailField(verbose_name="email")

    phone_validator = RegexValidator(regex=r"^[0-9\+]{11,12}$", message="+79994443322")
    phone = models.CharField(
        max_length=12, verbose_name="контактный телефон", validators=[phone_validator]
    )

    def __str__(self):
        return (
            f"<Отклик от: {self.full_name} на: "
            f"{self.product_option.product.name} "
            f"категория: {self.product_option.product.category.name}>"
        )
