from django.contrib.auth.backends import BaseBackend

from .models import Company


class CompanyBackend(BaseBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(Company.USERNAME_FIELD)
        if username is None or password is None:
            return
        try:
            user = Company._default_manager.get_by_natural_key(username)
        except Company.DoesNotExist:
            Company().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def user_can_authenticate(self, user):
        is_active = getattr(user, 'is_active', None)
        return is_active or is_active is None

    def get_user(self, user_id):
        try:
            user = Company._default_manager.get(pk=user_id)
        except Company.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None
