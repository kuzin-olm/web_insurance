from django.urls import include, path

from .views import (
    ProductOptionView,
    ProductOptionDetailView,
    ProductOptionDeleteView,
    ProductOptionUpdateView,
)


urlpatterns = [
    path("", ProductOptionView.as_view(), name="home"),
    path("product/<int:pk>/", ProductOptionDetailView.as_view(), name="product_detail"),
    path(
        "product/<int:pk>/delete",
        ProductOptionDeleteView.as_view(),
        name="product_delete",
    ),
    path(
        "product/<int:pk>/update",
        ProductOptionUpdateView.as_view(),
        name="product_update",
    ),
]
