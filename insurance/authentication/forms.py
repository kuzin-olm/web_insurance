from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django import forms

from users.models import Company


class CompanyCreationForm(UserCreationForm):

    class Meta:
        model = Company
        fields = ('name', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {
                'placeholder': 'Название компании',
                'class': 'form-control'
            }
        )
        self.fields['password1'].widget.attrs.update(
            {
                'placeholder': 'Пароль',
                'class': 'form-control',
                'id': 'password1'
            }
        )
        self.fields['password2'].widget.attrs.update(
            {
                'placeholder': 'Подтвердить пароль',
                'class': 'form-control',
                'id': 'password2'
            }
        )


class CompanyAuthenticationForm(AuthenticationForm):

    class Meta:
        model = Company
        fields = ('name', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {
                'placeholder': 'Название компании',
                'class': 'form-control'
            }
        )
        self.fields['password'].widget.attrs.update(
            {
                'placeholder': 'Пароль',
                'class': 'form-control',
                'id': 'password2'
            }
        )

    def authenticate(self, username=None, password=None):
        try:
            company = Company.objects.get(name=username)
            if company.check_password(password):
                return company
            return None
        except Company.DoesNotExist:
            return None

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = self.authenticate(username=username, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
