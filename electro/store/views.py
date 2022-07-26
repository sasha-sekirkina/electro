from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout

from .models import Product, Producer, Category, StoreInfo


# def test(request):
#     return render(request, 'base.html')


def index(request):
    products = Product.objects.filter(old_price__gt=F('price')).select_related('producer')
    producers = Producer.objects.all()
    context = {
        'special_title': 'Специальное предложение',
        'sale_badge': 'Скидки',
        'products': products,
        'producers': producers,
    }
    return render(request, 'store/index.html', context=context)


class ProductView(DetailView):
    model = Product
    template_name = 'store/product.html'
    context_object_name = 'item'


class Search(ListView):
    model = Product
    template_name = 'store/products_list.html'
    context_object_name = "products"
    paginate_by = 4

    def get_queryset(self):
        return Product.objects.filter(name__icontains=self.request.GET.get('search'))

    # нужен чтобы пагинация работала при поиске
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = f'search={self.request.GET.get("search")}&'
        return context


class ProductsByCategory(ListView):
    model = Product
    template_name = 'store/products_list.html'
    context_object_name = 'products'
    paginate_by = 4

    def get_queryset(self):
        return Product.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(slug=self.kwargs['slug'])
        return context


class FilteredProducts(ListView):
    model = Product
    template_name = 'store/products_list.html'
    context_object_name = "products"
    paginate_by = 4


    def get_queryset(self):
        query_to_show = Product.objects.all()
        req = set(self.request.GET)
        cat_slug = {'naushniki', 'noutbuki', 'smartfony', 'planshety'}
        lst_cat = list(cat_slug & req)
        if lst_cat:
            query_to_show = query_to_show.filter(category__slug__in=lst_cat)
        prod_name = {'Apple', 'Huawei', 'Samsung'}
        lst_prod = list(prod_name & req)
        if lst_prod:
            query_to_show = query_to_show.filter(producer__name__in=lst_prod)
        if self.request.GET.get('special'):
            query_to_show = query_to_show.filter(old_price__gt=F('price'))
        return query_to_show

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        lister = list(self.request.GET)
        string = '=1&'.join(lister)
        string += '=1&'
        context['s'] = string
        return context


def privacy_policy(request):
    info = StoreInfo.objects.get(pk=1)
    policy = info.privacy_policy
    return render(request, 'store/text.html', context={'text': policy})


def orders_and_returns(request):
    info = StoreInfo.objects.get(pk=1)
    orders_returns = info.orders_and_returns
    return render(request, 'store/text.html', context={'text': orders_returns})


def terms_and_conditions(request):
    info = StoreInfo.objects.get(pk=1)
    terms = info.terms_and_conditions
    return render(request, 'store/text.html', context={'text': terms})


def about_us(request):
    info = StoreInfo.objects.get(pk=1)
    about_us = info.about_us
    return render(request, 'store/text.html', context={'text': about_us})
