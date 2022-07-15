from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='home'),
    path('category/<slug:slug>/', ProductsByCategory.as_view(), name='bycategory'),
    path('brand/<slug:slug>/', ProductsByProducer.as_view(), name='byproducer'),
    # path('/', index),
]
