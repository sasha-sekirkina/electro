from django import template

from blog.models import Post, Category
from django.db.models import Count, F
from django.core.cache import cache

register = template.Library()

# cache
@register.simple_tag()
def get_categories():
    return cache.get_or_set('blog_categories', Category.objects.filter().annotate(cnt=Count
    ('posts', filter=F('posts__is_published'))).filter(cnt__gt=0))
