from django.contrib.auth.models import User
from django.db import models

from django.urls import reverse_lazy, reverse

from user.models import Profile


class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(is_available=True)


def get_product_image_path(instance, filename):
    return f'products/{instance.category}/{instance.name}/{filename}'


def get_producer_image_path(instance, filename):
    return f'producers/{instance.name}/{filename}'


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(max_length=420, blank=True)
    characteristics = models.TextField(max_length=2000, blank=True)
    photo = models.ImageField(upload_to=get_product_image_path, verbose_name='Фото')
    price = models.IntegerField(verbose_name='Цена')
    sale = models.BooleanField(default=False)
    old_price = models.IntegerField(verbose_name='Старая цена')
    is_available = models.BooleanField(default=True, verbose_name='Наличие')
    amount = models.IntegerField(verbose_name='Количество')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')
    producer = models.ForeignKey('Producer', on_delete=models.PROTECT, verbose_name='Производитель')
    slug = models.SlugField(db_index=True, unique=True)
    users_wishlist = models.ManyToManyField(User, related_name='user_wishlist', blank=True)
    objects = models.Manager()
    products = ProductManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        default_related_name = 'products'
        ordering = ['price']

    def get_absolute_url(self):
        return reverse('store:prod_view', kwargs={'pk': self.pk})


class Producer(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Производитель')
    logo = models.ImageField(upload_to=get_producer_image_path, blank=True)
    slug = models.SlugField(db_index=True, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Производитель(я)'
        verbose_name_plural = 'Производители'

    def get_absolute_url(self):
        return reverse_lazy('store:prdcr', kwargs={'slug': self.slug})


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(db_index=True, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория(ю)'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse('store:bycategory', kwargs={'slug': self.slug})


class StoreInfo(models.Model):
    logo = models.ImageField(max_length=250)

    name = models.CharField(max_length=150)
    address = models.CharField(max_length=150)
    phone = models.CharField(max_length=150)
    short_description = models.CharField(max_length=250)
    email = models.EmailField(max_length=150)

    about_us = models.TextField(max_length=2500)
    privacy_policy = models.TextField(max_length=2500)
    orders_and_returns = models.TextField(max_length=2500)
    terms_and_conditions = models.TextField(max_length=2500)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Информация о магазине'
        verbose_name_plural = 'Информация о магазине'
