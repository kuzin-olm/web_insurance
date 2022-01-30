from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import CompanyCreationForm, CompanyAuthenticationForm


def register(request):

    if request.method == "POST":
        form = CompanyCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = CompanyCreationForm()

    return render(request, "auth/register.html", {"form": form})


class CompanyLoginView(LoginView):

    authentication_form = CompanyAuthenticationForm
    template_name = "auth/login.html"


class CompanyLogoutView(LogoutView):
    next_page = reverse_lazy("home")
