from django.urls import path

from .views import *

app_name = 'cart'

urlpatterns = [
    path('', cart, name='cart'),
    path('change/', cart_change, name='cart_change'),
]