from django import template

from store.models import Category, Producer, Product
from django.db.models import Count, F


register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.filter().annotate(cnt=Count('products', filter=F('products__is_available'))).filter(cnt__gt=0)


