# Generated by Django 4.0.6 on 2022-07-15 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='old_price',
            field=models.IntegerField(default=1, verbose_name='Старая цена'),
            preserve_default=False,
        ),
    ]
