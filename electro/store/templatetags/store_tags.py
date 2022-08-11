from django import template

from store.models import Category, Producer, Product, StoreInfo
from blog.models import Post
from django.db.models import Count, F
from django.core.cache import cache

register = template.Library()


# cache
@register.simple_tag()
def get_categories():
    return cache.get_or_set('store_categories', Category.objects.filter().annotate(cnt=Count
    ('products', filter=F('products__is_available'))).filter(cnt__gt=0))


@register.simple_tag()
def get_store_info():
    # return cache.get_or_set('store_information', StoreInfo.objects.get(pk=1))
    return StoreInfo.objects.get(pk=1)


# cache
@register.simple_tag()
def get_producers():
    return cache.get_or_set('store_producers', Producer.objects.filter().annotate(cnt=Count
    ('products', filter=F('products__is_available'))).filter(cnt__gt=0))


# cache and select_related
@register.inclusion_tag('store/tags/special_offer.html')
def show_special_offer_products():
    import random
    products = cache.get_or_set('special_offer_index', Product.objects.filter(
        sale=True, is_available=True).select_related('category', 'producer'), 20)
    indexes = range(1, len(products))
    chosen_indexes = random.sample(indexes, 5)
    products_set = set()
    for item in chosen_indexes:
        products_set.add(products[item])
    context = {'products': products_set,
               'title': 'Специальное предложение'}
    return context


# cache and select_related
@register.inclusion_tag('store/tags/blog_desc.html')
def show_blog_posts():
    posts = cache.get_or_set('posts_index',
                             Post.objects.all()[:3].select_related('category'), 20)
    context = {'posts': posts,
               'title': 'Check out latest posts!!!'}
    return context

# @register.inclusion_tag('store/show_producers.html')
# def show_producers():
#     # categories = cache.get_or_set('categories', Category.objects.filter(
#     ).annotate(cnt=Count('news', filter=F('news__is_published'))).filter(cnt__gt=0), 30)
#     producers = Producer.objects.filter().annotate(cnt=Count('products', filter=F(
#     'products__is_available'))).filter(cnt__gt=0)
#     return {'producers': producers}
#
# @register.inclusion_tag('store/show_categories.html')
# def show_categories():
#     # categories = cache.get_or_set('categories', Category.objects.filter().annotate(
#     cnt=Count('news', filter=F('news__is_published'))).filter(cnt__gt=0), 30)
#     categories = Category.objects.filter().annotate(cnt=Count('products', filter=F(
#     'products__is_available'))).filter(cnt__gt=0)
#     return {'categories': categories}
