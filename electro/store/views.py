from django.core.paginator import Paginator
from django.db.models import F, Count
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView

from .models import Product, Producer, Category, StoreInfo


def get_set(model, field):
    # возвращает сет со всеми слагами или именами (field), объекты готорых которых содержат
    # хотя бы один продукт
    needed = model.objects.filter().annotate(cnt=Count('products', filter=F(
        'products__is_available'))).filter(
        cnt__gt=0)
    slugs = set()
    for item in needed:
        eval(f'slugs.add(item.{field})')
    return slugs


def get_store_information(request, field):
    info = StoreInfo.objects.get(pk=1)
    text = eval(f'info.{field}')
    return render(request, 'store/text.html', context={'text': text})


def index(request):
    return render(request, 'store/index.html')


class ProductsByCategory(ListView):
    model = Product
    template_name = 'store/products_list.html'
    context_object_name = 'products'
    paginate_by = 4

    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs['slug'], is_available=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(slug=self.kwargs['slug']).slug
        context['reqs'] = [category]
        return context


class FilteredProducts(ListView):
    model = Product
    template_name = 'store/products_list.html'
    context_object_name = "products"
    paginate_by = 4

    def get_queryset(self):
        query_to_show = Product.objects.filter(is_available=True)
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
        # TODO
        string = '=1&'.join(lister)
        string += '=1&'
        context['s'] = string
        context['reqs'] = lister
        if self.request.GET.get('special'):
            context['special'] = 1
        return context


# не смогла сделать пагинацию работающую

# def by_producer(request, producer_id):
#     products = Product.objects.filter(producer_id=producer_id)
#
#     paginator = Paginator(products, 4)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#
#     producer = Producer.objects.get(pk=producer_id).name
#     lister = [producer]
#     context = {
#         'products': products,
#         'reqs': lister,
#         'page_obj': page_obj,
#     }
#     return render(request, 'store/products_list.html', context=context)


class ProductsByProducer(ListView):
    model = Product
    template_name = 'store/products_list.html'
    context_object_name = "products"
    paginate_by = 4

    def get_queryset(self):
        return Product.objects.filter(producer_id=self.kwargs['producer_id'], is_available=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        producer = Producer.objects.get(pk=self.kwargs['producer_id']).name
        context['reqs'] = [producer]
        return context


# не смогла сделать пагинацию работающую
#
# def by_special(request):
#     products = Product.objects.filter(sale=True)
#
#     paginator = Paginator(products, 4)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#
#     context = {
#         'products': products,
#         'special': 1,
#         'page_obj': page_obj,
#     }
#     return render(request, 'store/products_list.html', context=context)


class ProductsBySpecialOffer(ListView):
    model = Product
    template_name = 'store/products_list.html'
    context_object_name = "products"
    paginate_by = 4

    def get_queryset(self):
        return Product.objects.filter(sale=True, is_available=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['special'] = 1
        return context


class Search(ListView):
    model = Product
    template_name = 'store/products_list.html'
    context_object_name = "products"
    paginate_by = 4

    def get_queryset(self):
        return Product.objects.filter(name__icontains=self.request.GET.get('search'), is_available=True)

    # нужен чтобы пагинация работала при поиске
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = f'search={self.request.GET.get("search")}&'
        return context


class ProductView(DetailView):
    model = Product
    template_name = 'store/product.html'
    context_object_name = 'item'


def privacy_policy(request):
    return get_store_information(request, 'privacy_policy')


def orders_and_returns(request):
    return get_store_information(request, 'orders_and_returns')


def terms_and_conditions(request):
    return get_store_information(request, 'terms_and_conditions')


def about_us(request):
    return get_store_information(request, 'about_us')

# older, before i created get_store_information
#
# def orders_and_returns(request):
#     info = StoreInfo.objects.get(pk=1)
#     orders_returns = info.orders_and_returns
#     return render(request, 'store/text.html', context={'text': orders_returns})
