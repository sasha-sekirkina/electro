from django import template

from blog.models import Post, Category
from django.db.models import Count, F

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.filter().annotate(cnt=Count('posts', filter=F('posts__is_published'))).filter(cnt__gt=0)
