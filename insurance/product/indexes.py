from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .models import ProductOption, Product, ProductCategory
from users.models import Company


@registry.register_document
class ProductOptionDocument(Document):

    product = fields.ObjectField(
        properties={
            "category": fields.ObjectField(properties={"name": fields.TextField()}),
            "company": fields.ObjectField(properties={"name": fields.TextField()}),
            "name": fields.TextField(),
            "description": fields.TextField(),
            "is_active": fields.BooleanField(),
        }
    )

    class Index:
        name = "product_option"

    class Django:
        model = ProductOption
        fields = ["id", "price", "expire", "rate", "is_active"]

        # related_models = [Product, ProductCategory, Company]
