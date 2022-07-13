from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='home'),
    path('category/<slug:slug>/', ProductsByCategory.as_view(), name='bycategory')
    # path('/', index),
]
