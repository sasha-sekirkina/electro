# Generated by Django 4.0.6 on 2022-08-09 09:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_remove_profile_wishlist_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Wishlist',
        ),
    ]
