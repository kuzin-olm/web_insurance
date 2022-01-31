from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DeleteView, UpdateView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from .models import ProductOption


class ProductOptionView(ListView):
    model = ProductOption
    template_name = "product/index.html"


class ProductOptionDetailView(DeleteView):
    model = ProductOption
    context_object_name = "product_option"
    template_name = "product/view.html"


class ProductOptionUpdateView(UpdateView):
    pass


class ProductOptionDeleteView(DeleteView):
    model = ProductOption
    success_url = reverse_lazy("home")

    # def post(self, request, *args, **kwargs):
    #     product_option = self.model.objects.get(pk=self.kwargs.get('pk'))
    #     if request.user == product_option.product.company:
    #         return super().post(request, *args, **kwargs)
    #     return reverse_lazy("product_detail", pk=self.kwargs.get('pk'))
