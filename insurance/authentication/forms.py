from django.contrib.auth import login, authenticate
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
