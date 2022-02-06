from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from .managers import CompanyManager


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
