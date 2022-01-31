from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from .managers import CompanyManager
import django.contrib.auth.views

# class CompanyUser(AbstractUser):
#
#     username_validator = UnicodeUsernameValidator()
#
#     username = models.CharField(
#         _('username'),
#         max_length=150,
#         help_text=_('Необходимо. 150 символов или меньше. Только буквы, цифры и @/./+/-/_.'),
#         validators=[username_validator],
#         error_messages={
#             'unique': _("A user with that username already exists."),
#         },
#     )
#     email = models.EmailField(
#         _('email address'),
#         unique=True,
#         error_messages={
#             'unique': _("A user with that username already exists."),
#         },
#     )
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []
#
#     objects = CompanyUserManager()
#
#     def __str__(self):
#         return self.email


class Company(AbstractBaseUser):

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
            "unique": _("Такая компания уже зарегестрированна."),
        },
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Указывает, следует ли считать этого пользователя активным. "
            "Отмените выбор вместо удаления учетных записей."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = CompanyManager()

    USERNAME_FIELD = "name"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("компания")
        verbose_name_plural = _("компании")
