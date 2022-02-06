from django.urls import path


from .views import CompanyLoginView, CompanyLogoutView, CompanyRegisterView


urlpatterns = [
    path(
        "reg/",
        CompanyRegisterView.as_view(),
        name="company_registration",
    ),
    path("login/", CompanyLoginView.as_view(), name="company_login"),
    path("logout/", CompanyLogoutView.as_view(), name="company_logout"),
]
