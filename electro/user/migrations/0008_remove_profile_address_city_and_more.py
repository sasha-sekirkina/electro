# Generated by Django 4.0.6 on 2022-08-08 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_remove_profile_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='address_city',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='address_country',
        ),
        migrations.AddField(
            model_name='profile',
            name='address_country_city',
            field=models.CharField(max_length=100, null=True, verbose_name='Страна'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='address_street',
            field=models.CharField(max_length=100, null=True, verbose_name='Улица, дом, кв'),
        ),
    ]
