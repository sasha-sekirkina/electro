from django.urls import path
from .views import *

app_name = 'store'

urlpatterns = [
    path('category/<slug:slug>/', ProductsByCategory.as_view(), name='bycategory'),
    path('product/<int:pk>/', cache_page(30)(ProductView.as_view()), name='prod_view'),

    path('search/', Search.as_view(), name='search'),
    path('filtered/', FilteredProducts.as_view(), name='fltrd'),
    path('producer/<slug:slug>', ProductsByProducer.as_view(), name='prdcr'),

    path('special_offer_all/', ProductsBySpecialOffer.as_view(), name='by_special'),

    path('privacy_policy', privacy_policy, name='ppol'),
    path('orders_and_returns', orders_and_returns, name='ord_ret'),
    path('terms_and_conditions', terms_and_conditions, name='terms'),
    path('about_us', about_us, name='about'),

]
