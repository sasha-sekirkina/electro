from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *

app_name = 'blog'

urlpatterns = [
    path('', Posts.as_view(), name='all_posts'),
    path('post/<slug:slug>/', cache_page(30)(PostDetail.as_view()), name='post'),
    path('posts/by_category/<slug:slug>/', PostsByCategory.as_view(), name='bycategory'),

    path('search/', BlogSearch.as_view(), name='search'),

]
