from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout

from .models import Product, Producer, Category


def index(request):
    products = Product.objects.filter(old_price__gt=F('price')).select_related('producer')
    producers = Producer.objects.all()
    context = {
        'special_title' : 'Специальное предложение',
        'sale_badge': 'Скидки',
        'products': products,
        'producers': producers,
    }
    return render(request, 'store/index.html', context=context)


class ProductsByCategory(ListView):
    model = Product
    template_name = 'store/category_list.html'
    context_object_name = 'products'
    paginate_by = 4

    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs['slug'], is_available=True).select_related(
            'category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(slug=self.kwargs['slug'])
        return context


class ProductsByProducer(ListView):
    pass
