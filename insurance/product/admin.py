from django.contrib import admin

from .models import ProductCategory, Product, ProductOption, ProductResponse

admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(ProductOption)
admin.site.register(ProductResponse)
