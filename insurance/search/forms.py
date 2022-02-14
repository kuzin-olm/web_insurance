from django import forms
from product.models import ProductCategory
from users.models import Company


class SearchFilterForm(forms.Form):
    COMPANY_CHOICES = [
        (None, "-----"),
    ]
    CATEGORY_CHOICES = [
        (None, "-----"),
    ]

    COMPANY_CHOICES += [
        (company.name, company.name) for company in Company.objects.all()
    ]
    CATEGORY_CHOICES += [
        (category.name, category.name) for category in ProductCategory.objects.all()
    ]

    price_gte = forms.FloatField(
        required=False, widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    price_lte = forms.FloatField(
        required=False, widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    expire_gte = forms.IntegerField(
        required=False, widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    expire_lte = forms.IntegerField(
        required=False, widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    rate_gte = forms.FloatField(
        required=False, widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    rate_lte = forms.FloatField(
        required=False, widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    company = forms.ChoiceField(
        choices=COMPANY_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
