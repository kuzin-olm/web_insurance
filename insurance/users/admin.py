from django.contrib import admin
from django.contrib.auth.models import Group
from django import forms

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import Company, User, Worker
from authentication.forms import UserCreationForm

admin.site.register(Company)
admin.site.register(Worker)


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ("email", "username", "password", "is_active", "is_admin")


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ("email", "username", "is_admin")
    list_filter = ("is_admin",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("username",)}),
        ("Permissions", {"fields": ("is_admin",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "password1", "password2"),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
