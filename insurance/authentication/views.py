from django.contrib.auth import authenticate, login
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

from .forms import CompanyCreationForm, CompanyAuthenticationForm
from users.models import Company


class CompanyRegisterView(CreateView):
    model = Company
    template_name = "auth/register.html"
    form_class = CompanyCreationForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form_edit = super().form_valid(form)

        username = form.cleaned_data.get("name")
        password = form.cleaned_data.get("password2")

        if username and password:
            company_cache = authenticate(
                username=username,
                password=password,
                backend="users.backend.CompanyBackend",
            )
            if company_cache:
                login(
                    self.request, company_cache, backend="users.backend.CompanyBackend"
                )

        return form_edit


class CompanyLoginView(LoginView):

    authentication_form = CompanyAuthenticationForm
    template_name = "auth/login.html"


class CompanyLogoutView(LogoutView):
    next_page = reverse_lazy("home")
