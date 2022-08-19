from django.contrib.auth.models import User
from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver


def get_user_photo_path(instance, filename):
    return f'users/{instance.id}/{filename}'


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    phone = models.PositiveIntegerField(
        verbose_name='Телефон',
        null=True,
    )
    birth_date = models.DateField(
        blank=True,
        verbose_name='Дата рождения',
        null=True,
    )
    newsletter_subscription = models.BooleanField(
        verbose_name='Подписка',
        default=True,
        null=True,
    )
    is_active = models.BooleanField(
        verbose_name='Подтвержден',
        default=False,
    )
    # orders = models.ManyToManyField('Order', verbose_name='Заказы', null=True)
    address_country_city = models.CharField(
        max_length=100,
        null=True,
        verbose_name='Страна, город',
    )
    address_street = models.CharField(
        max_length=100,
        null=True,
        verbose_name='Улица, дом, кв',
    )
    address_zip = models.PositiveIntegerField(
        null=True,
        verbose_name='Почтовый индекс',
    )
    user_comments = models.TextField(
        null=True,
        verbose_name='Комментарии пользователя',
    )
    store_comments = models.TextField(
        null=True,
        verbose_name='Комментарии магазина',
    )

    def __str__(self):
        return f'Profile for {self.user.username}'

    # def get_absolute_url(self):
    #     return reverse('user:profile', kwargs={'username': self.user.username})

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
