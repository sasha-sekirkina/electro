from django.urls import path, include
from django.views.generic import TemplateView

from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetView

from electro import settings
from .views import *

app_name = 'user'

password_urls = [
    path('change/', UserPasswordChange.as_view(), name='pass_change'),
    path('reset/', PasswordResetView.as_view(
        template_name='user/password_reset.html',
        email_template_name='user/emails/password_reset_email.html',
        success_url='password_reset_email_confirm',
        from_email=settings.EMAIL_HOST_USER,
        form_class=UserPasswordResetForm), name='pass_reset'),
    path('password_reset_confirm/<slug:uidb64>/<slug:token>/', PasswordResetConfirmView.as_view(
        template_name='user/password_reset_confirm.html',
        success_url='/user/password/password_reset_complete',
        form_class=UserPasswordResetConfirmForm), name='pass_reset_confirm'),

    path('reset/password_reset_email_confirm/', TemplateView.as_view(
        template_name="user/password_reset_status.html"), name='password_reset_done'),

    path('password_reset_complete/', TemplateView.as_view(
        template_name="user/password_reset_status.html"), name='password_reset_complete'),
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
    # path('login/', LoginView.as_view(template_name='user/login.html',
    #                                  form_class=UserLoginForm,
    #                                  next_page='home') , name='login'),
    path('login/', UserLogin.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(template_name='user/logout.html',
    #                                    next_page='user:login'), name='logout'),
    path('logout/', user_logout, name='logout'),
    path('profile/', include(profile_urls)),
    path('password/', include(password_urls)),
    path('activate/<slug:uidb64>/<slug:token>/', activation_success, name='activate')
]
