from django import template

from store.models import Category, Producer, Product, StoreInfo
from django.db.models import Count, F

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.filter().annotate(cnt=Count('products', filter=F('products__is_available'))).filter(
        cnt__gt=0)


@register.simple_tag()
def get_store_info():
    return StoreInfo.objects.get(pk=1)


@register.simple_tag()
def get_producers():
    return Producer.objects.filter().annotate(cnt=Count('products', filter=F('products__is_available'))).filter(
        cnt__gt=0)

# @register.inclusion_tag('store/show_producers.html')
# def show_producers():
#     # categories = cache.get_or_set('categories', Category.objects.filter().annotate(cnt=Count('news', filter=F('news__is_published'))).filter(cnt__gt=0), 30)
#     producers = Producer.objects.filter().annotate(cnt=Count('products', filter=F('products__is_available'))).filter(cnt__gt=0)
#     return {'producers': producers}
#
# @register.inclusion_tag('store/show_categories.html')
# def show_categories():
#     # categories = cache.get_or_set('categories', Category.objects.filter().annotate(cnt=Count('news', filter=F('news__is_published'))).filter(cnt__gt=0), 30)
#     categories = Category.objects.filter().annotate(cnt=Count('products', filter=F('products__is_available'))).filter(cnt__gt=0)
#     return {'categories': categories}
