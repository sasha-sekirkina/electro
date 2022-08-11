from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView

from store.models import Product
from .forms import *


def user_orders(request):
    context = {
        'info': 'orders',
    }
    return render(request, 'user/profile.html', context)


# ----------------------------------------------------------------------------------------------


class UserRegister(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'user/register.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('user:login')
        else:
            messages.error(request, 'Ошибка регистрации')


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
    else:
        product.users_wishlist.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


class Wishlist(LoginRequiredMixin, ListView):
    login_url = 'user:login'
    template_name = 'user/user_wish_list.html'
    context_object_name = 'wishlist'
    paginate_by = 5

    def get_queryset(self):
        return Product.objects.filter(users_wishlist=self.request.user)
