from django.urls import path

from .views import *

app_name = 'cart'

urlpatterns = [
    path('', cart, name='cart'),
    path('add_to_cart/', add_to_cart, name='add_to_cart'),
]