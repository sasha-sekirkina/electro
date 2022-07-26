from django.urls import path, include
from .views import *

urlpatterns = [
    # path('test', test),
    path('', index, name='home'),
    path('filtered/', FilteredProducts.as_view(), name='fltrd'),

    path('category/<slug:slug>/', ProductsByCategory.as_view(), name='bycategory'),
    path('product/<int:pk>/', ProductView.as_view(), name='prod_view'),

    path('privacy_policy', privacy_policy, name='ppol'),
    path('orders_and_returns', orders_and_returns, name='ord_ret'),
    path('terms_and_conditions', terms_and_conditions, name='terms'),
    path('about_us', about_us, name='about'),

    path('search/', Search.as_view(), name='search'),
]
