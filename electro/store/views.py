from django.contrib.auth.forms import UserCreationForm
from django.core.cache import cache
# from django.views.decorators.cache import cache_page
# from django.core.paginator import Paginator
from django.db.models import F, Count
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView, CreateView
from django.contrib import messages

from .models import Product, Producer, Category, StoreInfo


# cache
def get_set(model, field):
    # возвращает сет из полей (field) всех объектов указанной модели (model),
    # с которыми связан хотя бы один продукт

    needed = cache.get_or_set(f'set_{model}', model.objects.filter().annotate(cnt=Count(
        'products', filter=F('products__is_available'))).filter(cnt__gt=0))

    # needed = model.objects.filter().annotate(cnt=Count('products', filter=F(
    #     'products__is_available'))).filter(cnt__gt=0)
    slugs = set()
    for item in needed:
        eval(f'slugs.add(item.{field})')
    return slugs


def index(request):
    return render(request, 'store/index.html')


# select_related
class ProductsByCategory(ListView):
    model = Product
    template_name = 'store/products_list.html'
    context_object_name = 'products'
    paginate_by = 4

    def get_queryset(self):
        return Product.products.filter(category__slug=self.kwargs['slug']).select_related(
            'category', 'producer')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.kwargs['slug']
        context['reqs'] = [category]
        return context


# select_related
class FilteredProducts(ListView):
    model = Product
    template_name = 'store/products_list.html'
    context_object_name = "products"
    paginate_by = 4

    def get_queryset(self):
        query_to_show = Product.products.all().select_related('category', 'producer')
        req = set(self.request.GET)
        cat_slug = get_set(Category, 'slug')
        lst_cat = list(cat_slug & req)
        if lst_cat:
            query_to_show = query_to_show.filter(category__slug__in=lst_cat)

        prod_name = get_set(Producer, 'name')
        lst_prod = list(prod_name & req)
        if lst_prod:
            query_to_show = query_to_show.filter(producer__name__in=lst_prod)

        if self.request.GET.get('special'):
            query_to_show = query_to_show.filter(sale=True)
        return query_to_show

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        lister = list(self.request.GET)
        string = '=1&'.join(lister)
        string += '=1&'
        context['s'] = string
        context['reqs'] = lister
        if self.request.GET.get('special'):
            context['special'] = 1
        return context


# select_related
class ProductsByProducer(ListView):
    model = Product
    template_name = 'store/products_list.html'
    context_object_name = "products"
    paginate_by = 4

    def get_queryset(self):
        return Product.products.filter(producer__slug=self.kwargs['slug']).select_related(
            'category', 'producer')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        producer = Producer.objects.get(slug=self.kwargs['slug']).name
        context['reqs'] = [producer]
        return context


# select_related
class ProductsBySpecialOffer(ListView):
    model = Product
    template_name = 'store/products_list.html'
    context_object_name = "products"
    paginate_by = 4

    def get_queryset(self):
        return Product.products.filter(sale=True).select_related('category', 'producer')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['special'] = 1
        return context


# select_related
class Search(ListView):
    model = Product
    template_name = 'store/products_list.html'
    context_object_name = "products"
    paginate_by = 4

    def get_queryset(self):
        return Product.products.filter(name__icontains=self.request.GET.get(
            'search')).select_related('category', 'producer')

    # нужен чтобы пагинация работала при поиске
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = f'search={self.request.GET.get("search")}&'
        return context


class ProductView(DetailView):
    model = Product
    template_name = 'store/product.html'
    context_object_name = 'item'


@cache_page(20)
def privacy_policy(request):
    text = StoreInfo.objects.get(pk=1).privacy_policy
    return render(request, 'store/text.html', context={'text': text})


@cache_page(20)
def orders_and_returns(request):
    text = StoreInfo.objects.get(pk=1).orders_and_returns
    return render(request, 'store/text.html', context={'text': text})


@cache_page(20)
def terms_and_conditions(request):
    text = StoreInfo.objects.get(pk=1).terms_and_conditions
    return render(request, 'store/text.html', context={'text': text})


@cache_page(20)
def about_us(request):
    text = StoreInfo.objects.get(pk=1).about_us
    return render(request, 'store/text.html', context={'text': text})
