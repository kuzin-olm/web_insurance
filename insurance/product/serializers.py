from .models import ProductResponse

from django.forms.models import model_to_dict


def product_response_serialize(product_response: ProductResponse):

    data = model_to_dict(product_response)
    data["company_email"] = product_response.product_option.product.company.email

    return data
