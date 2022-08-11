from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django import forms

from .models import Profile


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'autocomplete': 'off', 'autofocus': 'none'}
        )
    )
    email = forms.EmailField(
        label='Электронная почта',
        widget=forms.EmailInput(
            attrs={'class': 'form-control'}
        )
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )
    password2 = forms.CharField(
        label='Подтвердите пароль',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control'}
        )
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserPasswordChangeForm(PasswordChangeForm):
    error_messages = {
        "password_mismatch": "Пароли не совпадает, повторите попытку",
        "password_incorrect": "Пароль введен неверно, повторите попытку",
    }
    old_password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "autocomplete": "current-password", "autofocus": True}
        )
    )
    new_password1 = forms.CharField(
        label='Новый пароль',
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "autocomplete": "new-password"}
        )
    )
    new_password2 = forms.CharField(
        label='Подтвердите новый пароль',
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "autocomplete": "new-password"}
        )
    )


class UserGeneralSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
        widgets = {
            'email': forms.EmailInput(
                attrs={'class': 'form-control'}
            ),
            'first_name': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control'}
            )
        }
        labels = {
            'email': 'Электронная почта',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }


class ProfileGeneralSettingsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'birth_date', 'newsletter_subscription']
        widgets = {
            'phone': forms.NumberInput(
                attrs={'class': 'form-control'}
            ),
            'birth_date': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'newsletter_subscription': forms.CheckboxInput(),
        }


class ProfileAddressSettingsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address_country_city', 'address_street', 'address_zip']
        widgets = {
            'address_country_city': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'address_street': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'address_zip': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
        }
