from django.urls import include, path

from .views import (
    CompanyCreateView,
    ProductOptionView,
    ProductOptionDetailView,
    ProductOptionDeleteView,
    ProductOptionUpdateView,
    ProductOptionCreateView,
    ProductCreateView,
    ProductDetailView,
    ProductUpdateView,
    ProductDeleteView,
    CabinetView,
    ProductCategoryCreateView,
    ResponseSuccessView,
    ProductResponseView,
)


urlpatterns = [
    path("", ProductOptionView.as_view(), name="home"),
    path(
        "company/create/",
        CompanyCreateView.as_view(),
        name="company_create",
    ),
    path(
        "product_option/<int:pk>/",
        ProductOptionDetailView.as_view(),
        name="product_option_detail",
    ),
    path(
        "product_option/<int:pk>/delete",
        ProductOptionDeleteView.as_view(),
        name="product_option_delete",
    ),
    path(
        "product_option/<int:pk>/update",
        ProductOptionUpdateView.as_view(),
        name="product_option_update",
    ),
    path(
        "product_option/create",
        ProductOptionCreateView.as_view(),
        name="product_option_create",
    ),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path(
        "product/<int:pk>/delete",
        ProductDeleteView.as_view(),
        name="product_delete",
    ),
    path(
        "product/<int:pk>/update",
        ProductUpdateView.as_view(),
        name="product_update",
    ),
    path(
        "product/create",
        ProductCreateView.as_view(),
        name="product_create",
    ),
    path(
        "lk/",
        CabinetView.as_view(),
        name="lk_home",
    ),
    path(
        "category/create/",
        ProductCategoryCreateView.as_view(),
        name="product_category_create",
    ),
    path(
        "response/<int:pk>/success/",
        ResponseSuccessView.as_view(),
        name="product_response_success",
    ),
    path(
        "response/",
        ProductResponseView.as_view(),
        name="product_response",
    ),
]
