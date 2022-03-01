from django.urls import path

from .views import UserRegisterView, UserLogoutView, UserLoginView

urlpatterns = [
    path(
        "reg/",
        UserRegisterView.as_view(),
        name="user_registration",
    ),
    path("login/", UserLoginView.as_view(), name="user_login"),
    path("logout/", UserLogoutView.as_view(), name="user_logout"),
]
