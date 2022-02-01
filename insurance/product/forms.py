from django import forms

from .models import ProductOption


class ProductOptionForm(forms.ModelForm):
    class Meta:
        model = ProductOption
        fields = (
            "product",
            "price",
            "expire",
            "rate",
            "is_active",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["product"].widget.attrs.update({"class": "form-select"})
        self.fields["price"].widget.attrs.update({"class": "form-control"})
        self.fields["expire"].widget.attrs.update({"class": "form-control"})
        self.fields["rate"].widget.attrs.update({"class": "form-control"})
        self.fields["is_active"].widget.attrs.update({"class": "form-check-input"})
