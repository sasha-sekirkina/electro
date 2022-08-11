from django.urls import path, include

from .views import *

app_name = 'user'

password_urls = [
    path('change/', UserPasswordChange.as_view(), name='pass_change'),
    # path('reset/', django.contrib.auth.views.PasswordResetView.as_view(), name='pass_change'),
    # path('reset/done/', django.contrib.auth.views.PasswordResetDoneView.as_view(), name='pass_change_done'),
]

profile_urls = [
    path('general/', UserGeneralSettings.as_view(), name='general'),
    path('address/', UserAddressSettings.as_view(), name='address'),

    path('wishlist/', Wishlist.as_view(), name='wishlist'),
    path('wishlist/add/<int:id>/', add_to_wishlist, name='add_wishlist'),

    path('orders/', user_orders, name='orders'),
]

urlpatterns = [
    path('register/', UserRegister.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', include(profile_urls)),
    path('password/', include(password_urls)),
]

