from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


# class CompanyUserManager(BaseUserManager):
#     """
#     Диспетчер пользовательских моделей пользователей, где электронная почта является уникальным идентификатором
#     для аутентификации вместо имен пользователей.
#     """
#     def create_user(self, email, password, **extra_fields):
#         """
#         Создать и сохранитть пользователя с указанным адресом электронной почты и паролем.
#         """
#         if not email:
#             raise ValueError(_('Должна быть электронная почта'))
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save()
#         return user
#
#     def create_superuser(self, email, password, **extra_fields):
#         """
#         Создать и сохранить суперпользователя с указанным адресом электронной почты и паролем.
#         """
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         extra_fields.setdefault('is_active', True)
#
#         if extra_fields.get('is_staff') is not True:
#             raise ValueError(_('Суперюзер должен быть is_staff=True.'))
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError(_('Суперюзер должен быть is_superuser=True.'))
#         return self.create_user(email, password, **extra_fields)


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
            raise ValueError(_('Должно быть имя компании'))
        company = self.model(name=name, **extra_fields)
        company.set_password(password)
        company.save()
        return company
