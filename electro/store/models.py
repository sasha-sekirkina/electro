from django.db import models


# from django.urls import reverse_lazy


def get_product_image_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/products/<instance.category>/<instance.name>/<filename>
    return f'products/{instance.category}/{instance.name}/{filename}'


def get_producer_image_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/producers/<instance.name>/<filename>
    return f'producers/{instance.name}/{filename}'


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(max_length=420, blank=True)
    photo = models.ImageField(upload_to=get_product_image_path, verbose_name='Фото')
    price = models.IntegerField(verbose_name='Цена')
    is_available = models.BooleanField(default=True, verbose_name='Наличие')
    amount = models.IntegerField(verbose_name='Количество')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')
    producer = models.ForeignKey('Producer', on_delete=models.PROTECT, verbose_name='Производитель')
    slug = models.SlugField(db_index=True, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        default_related_name = 'products'
        ordering = ['price']

    # def get_absolute_url(self):
    #     return reverse_lazy('procuct', kwargs={'producer_id': self.pk})


class Producer(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Производитель')
    logo = models.ImageField(upload_to=get_producer_image_path, blank=True)
    slug = models.SlugField(db_index=True, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Производитель(я)'
        verbose_name_plural = 'Производители'

    # def get_absolute_url(self):
    #     return reverse_lazy('producer', kwargs={'producer_id': self.pk})


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(db_index=True, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория(ю)'
        verbose_name_plural = 'Категории'

    # def get_absolute_url(self):
    #     return reverse_lazy('category', kwargs={'category_id': self.pk})
