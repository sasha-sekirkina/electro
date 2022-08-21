from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, PasswordResetView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import ListView

from electro.settings import EMAIL_HOST_USER
from store.models import Product
from .forms import *
from .token import account_activation_token


def user_orders(request):
    context = {
        'info': 'orders',
    }
    return render(request, 'user/profile.html', context)


# ----------------------------------------------------------------------------------------------


class UserRegister(View):
    def get(self, request):
        if request.user.is_authenticated:
            messages.info(request, 'Вы уже авторизованы')
            return redirect('home')
        form = UserRegisterForm()
        return render(request, 'user/register.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            current_site = get_current_site(request)
            subject = 'Activate your Account'
            message = render_to_string('user/emails/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            send_mail(
                subject,
                message,
                EMAIL_HOST_USER,
                (user.email,),
                fail_silently=False,
            )
            messages.success(request,
                             'Вы успешно зарегистрировались. Ссылка для активации отправлена на вашу электронную почту.')
            return redirect('user:login')
        else:
            messages.error(request, 'Ошибка регистрации')


def activation_success(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.profile.is_active = True
        user.profile.save()
        login(request, user)
        messages.success(request, 'Ваш аккаунт был успешно активирован')
        return redirect('home')
    else:
        return redirect('user/activation_invalid.html')


class UserLogin(View):
    def get(self, request):
        form = UserLoginForm()
        return render(request, 'user/login.html', {'form': form})

    def post(self, request):
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Ошибка авторизации')
        return render(request, 'user/login.html', {'form': form})


@login_required(login_url='user:login')
def user_logout(request):
    logout(request)
    return redirect('home')


class UserPasswordChange(LoginRequiredMixin, PasswordChangeView):
    login_url = 'user:login'
    form_class = UserPasswordChangeForm
    template_name = 'user/password_change.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Пароль успешно изменен')
        return reverse_lazy('user:profile')


class UserGeneralSettings(LoginRequiredMixin, View):
    login_url = 'user:login'

    def get(self, request):
        user_form = UserGeneralSettingsForm(instance=request.user)
        profile_form = ProfileGeneralSettingsForm(instance=request.user.profile)
        return render(request, 'user/user_general_settings.html', {
            'user_form': user_form,
            'profile_form': profile_form})

    def post(self, request):
        user_form = UserGeneralSettingsForm(request.POST, instance=request.user)
        profile_form = ProfileGeneralSettingsForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Ваш профиль был успешно обновлен!')
            return redirect('user:profile')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки.')


class UserAddressSettings(LoginRequiredMixin, View):
    login_url = 'user:login'

    def get(self, request):
        form = ProfileAddressSettingsForm(instance=request.user)
        return render(request, 'user/user_address_settings.html', {'form': form})

    def post(self, request):
        form = ProfileAddressSettingsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные были успешно изменены!')
            return redirect('user:address')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки')


@login_required(login_url='user:login')
def add_to_wishlist(request, id):
    product = get_object_or_404(Product, id=id)
    if product.users_wishlist.filter(id=request.user.id).exists():
        product.users_wishlist.remove(request.user)
        messages.info(request, '"' + product.name.upper() + '" удален из списка желаний')
    else:
        product.users_wishlist.add(request.user)
        messages.info(request, '"' + product.name.upper() + '" добавлен в список желаний')
    return render(request, 'store/product.html', {'item': product})


@login_required(login_url='user:login')
def remove_from_wishlist(request, id):
    product = get_object_or_404(Product, id=id)
    product.users_wishlist.remove(request.user)
    messages.info(request, '"' + product.name.upper() + '" удален из списка желаний')
    return redirect('user:wishlist')


class Wishlist(LoginRequiredMixin, ListView):
    login_url = 'user:login'
    template_name = 'user/user_wish_list.html'
    context_object_name = 'wishlist'
    paginate_by = 5

    def get_queryset(self):
        return Product.objects.filter(users_wishlist=self.request.user)
