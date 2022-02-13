from django.contrib.auth import authenticate, login
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

from users.models import User
from .forms import UserCreationForm, UserAuthenticationForm


class UserRegisterView(CreateView):
    model = User
    template_name = "auth/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form_edit = super().form_valid(form)

        email = form.cleaned_data.get("email")
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password2")

        if email and username and password:
            company_cache = authenticate(
                email=email,
                password=password,
            )
            if company_cache:
                login(self.request, company_cache)

        return form_edit


class UserLoginView(LoginView):

    authentication_form = UserAuthenticationForm
    template_name = "auth/login.html"


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("home")
