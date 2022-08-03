from django.db.models import *
from django.urls import reverse

from store.models import Product


def get_post_image_path(instance, filename):
    return f'posts/{instance.category}/{instance.title}/{filename}'


class Category(Model):
    title = CharField(max_length=100, verbose_name='Название')
    slug = SlugField(max_length=100, verbose_name='Url', db_index=True, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = 'Категория(ю)'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse('blog:bycategory', kwargs={'slug': self.slug})


class Post(Model):
    title = CharField(max_length=32, verbose_name='Заголовок')
    content = TextField(verbose_name='Контент', blank=True)
    short_description = CharField(max_length=126, verbose_name='Описание')
    main_photo = ImageField(upload_to=get_post_image_path, verbose_name='Обложка')
    created_at = DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_published = BooleanField(default=True)
    views = PositiveIntegerField(default=0, verbose_name='Просмотры')
    category = ForeignKey(Category, on_delete=SET_NULL, verbose_name='Категория', related_name='posts', null=True)
    slug = SlugField(max_length=100, verbose_name='Url', db_index=True, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def get_absolute_url(self):
        return reverse('blog:post', kwargs={'slug': self.slug})
