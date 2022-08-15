from django.urls import path

from .views import *

app_name = 'cart'

urlpatterns = [
    path('', cart, name='cart'),
    path('change/', cart_change, name='cart_change'),
    # path('add/', add_to_cart, name='cart_add'),
    # path('delete/', delete_from_cart, name='cart_delete'),
    # path('update/', update_cart, name='cart_update'),
]