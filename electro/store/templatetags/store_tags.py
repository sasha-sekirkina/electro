from django import template

from store.models import Category, Producer, Product, StoreInfo
from django.db.models import Count, F


register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.filter().annotate(cnt=Count('products', filter=F('products__is_available'))).filter(cnt__gt=0)


@register.simple_tag()
def get_store_info():
    return StoreInfo.objects.get(pk=1)

@register.simple_tag()
def get_producers():
    return Producer.objects.filter().annotate(cnt=Count('products', filter=F('products__is_available'))).filter(cnt__gt=0)