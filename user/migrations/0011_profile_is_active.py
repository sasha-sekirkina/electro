# Generated by Django 4.0.6 on 2022-08-16 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_delete_wishlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='Подтвержден'),
        ),
    ]
