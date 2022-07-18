from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='home'),
    path('category/<slug:slug>/', ProductsByCategory.as_view(), name='bycategory'),
    path('brand/<slug:slug>/', ProductsByProducer.as_view(), name='byproducer'),
    # path('/', index),
    path('privacy_policy', privacy_policy, name='ppol'),
    path('orders_and_returns', orders_and_returns, name='ord_ret'),
    path('terms_and_conditions', terms_and_conditions, name='terms'),
]
