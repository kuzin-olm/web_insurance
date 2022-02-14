from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from product.indexes import ProductOptionDocument
from elasticsearch_dsl import Q

from .forms import SearchFilterForm


class SearchView(TemplateView):
    template_name = "search/result.html"

    def get(self, request, *args, **kwargs):
        search = request.GET.get("q")

        if search:
            search_result = ProductOptionDocument.search().query(
                Q(
                    "bool",
                    should=[
                        Q(
                            "multi_match",
                            query=search,
                            fields=[
                                "product.description^2",
                                "product.name",
                                "product.category.name",
                                "product.company.name",
                            ],
                        ),
                        Q("prefix", product__description=search),
                        Q("prefix", product__category__name=search),
                        Q("prefix", product__company__name=search),
                    ],
                )
            )

            kwargs["search_results"] = search_result if search_result.count() else None
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        filter_form = SearchFilterForm(request.POST)
        if filter_form.is_valid():

            category = filter_form.cleaned_data["category"]
            company = filter_form.cleaned_data["company"]
            price_gte = filter_form.cleaned_data["price_gte"]
            price_lte = filter_form.cleaned_data["price_lte"]
            expire_gte = filter_form.cleaned_data["expire_gte"]
            expire_lte = filter_form.cleaned_data["expire_lte"]
            rate_gte = filter_form.cleaned_data["rate_gte"]
            rate_lte = filter_form.cleaned_data["rate_lte"]

            query_search = []
            if category:
                query_search.append(Q("match", product__category__name=category))
            if company:
                query_search.append(Q("match", product__company__name=company))
            if price_gte:
                query_search.append(Q("range", price={"gte": price_gte}))
            if price_lte:
                query_search.append(Q("range", price={"lte": price_lte}))
            if expire_gte:
                query_search.append(Q("range", expire={"gte": expire_gte}))
            if expire_lte:
                query_search.append(Q("range", expire={"lte": expire_lte}))
            if rate_gte:
                query_search.append(Q("range", rate={"gte": rate_gte}))
            if rate_lte:
                query_search.append(Q("range", rate={"lte": rate_lte}))

            search_result = ProductOptionDocument.search().query(
                Q(
                    "bool",
                    must=query_search,
                )
            )

            kwargs["search_results"] = search_result if search_result.count() else None
        return super().get(request, *args, **kwargs)
