from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from .managers import UserManager


class Company(models.Model):

    name_validator = UnicodeUsernameValidator()

    name = models.CharField(
        _("name"),
        max_length=150,
        unique=True,
        help_text=_(
            "Необходимо. 150 символов или меньше. Только буквы, цифры и @/./+/-/_."
        ),
        validators=[name_validator],
        error_messages={
            "unique": "Такая компания уже зарегестрированна.",
        },
    )

    email = models.EmailField(verbose_name="email компании")

    registration_date = models.DateTimeField("дата регистрации", default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "компания"
        verbose_name_plural = "компании"


class User(AbstractBaseUser):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        verbose_name="имя пользователя",
        max_length=255,
        help_text="Обязательное поле. Не более 255 символов. "
        "Только буквы, цифры и символы @/./+/-/_.",
        validators=[username_validator],
    )
    email = models.EmailField(verbose_name="e-mail", max_length=255, unique=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(
        "Активный",
        default=True,
        help_text=_(
            "Отметьте, если пользователь должен считаться активным."
            " Уберите эту отметку вместо удаления учётной записи."
        ),
    )
    registration_date = models.DateTimeField(
        verbose_name="дата регистрации", default=timezone.now
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """User have a specific permission."""
        return self.is_admin

    def has_module_perms(self, app_label):
        """User have permissions to view the app `app_label`."""
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Worker(models.Model):

    user = models.OneToOneField(to=User, on_delete=models.CASCADE, verbose_name="работник")
    company = models.ForeignKey(
        to=Company,
        on_delete=models.CASCADE,
        verbose_name="компания",
    )
    is_owner = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Работник"
        verbose_name_plural = "Работники"
