from django.urls import include, path


from .views import register, CompanyLoginView, CompanyLogoutView


urlpatterns = [
    path(
        'reg/',
        register,
        name='company_registration',
    ),
    path(
        'login/',
        CompanyLoginView.as_view(),
        name='company_login'
    ),
    path(
        'logout/',
        CompanyLogoutView.as_view(),
        name='company_logout'
    ),

]
