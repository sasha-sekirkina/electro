# Generated by Django 4.0.6 on 2022-08-03 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_alter_post_short_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='short_description',
            field=models.CharField(max_length=126, verbose_name='Описание'),
        ),
    ]