from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class CompanyManager(BaseUserManager):
    """
    Диспетчер моделей компаний, где имя является уникальным идентификатором
    для аутентификации.
    """

    def create(self, name, password, **extra_fields):
        """
        Создать и сохранитть компанию с указанными именем и паролем.
        """
        if not name:
            raise ValueError(_("Должно быть имя компании"))
        company = self.model(name=name, **extra_fields)
        company.set_password(password)
        company.save()
        return company
