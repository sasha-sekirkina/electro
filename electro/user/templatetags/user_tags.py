from django import template
from django.urls import reverse

from blog.models import Post
from django.db.models import Count, F
from django.core.cache import cache

register = template.Library()


@register.simple_tag()
def get_sections():
    context = (
        (reverse('home'), 'Магазин! '),
        (reverse('user:general'), 'Настройки'),
        (reverse('user:wishlist'), 'Желания'),
        (reverse('user:address'), 'Адрес'),
        (reverse('user:orders'), 'Заказы'),
    )
    return context
