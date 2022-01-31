from django.urls import include, path

from .views import ProductOptionView, ProductOptionDetailView


urlpatterns = [
    path("", ProductOptionView.as_view(), name="home"),
    path("product/<int:pk>/", ProductOptionDetailView.as_view(), name="product_detail"),
]
