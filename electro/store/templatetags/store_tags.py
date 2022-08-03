from django import template

from store.models import Category, Producer, Product, StoreInfo
from blog.models import Post
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


@register.inclusion_tag('store/tags/special_offer.html')
def show_special_offer_products():
    import random
    products = Product.objects.filter(sale=True, is_available=True)
    indexes = range(1, len(products))
    chosen_indexes = random.sample(indexes, 5)
    products_set = set()
    for item in chosen_indexes:
        products_set.add(products[item])

    context = {'products': products_set}
    context['title'] = 'Специальное предложение'
    return context


@register.inclusion_tag('store/tags/blog_desc.html')
def show_blog_posts():
    posts = Post.objects.all()[:3]
    context = {'posts': posts }
    context['title'] = 'Check out latest posts!!!'
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
