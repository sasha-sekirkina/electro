from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ('title', 'is_published', 'created_at', 'views', 'category')
    list_display_links = ('title',)
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('category',)
    list_select_related = True
    prepopulated_fields = {'slug': ('title',)}
    fields = ('title', 'slug','is_published', 'category',
               # 'get_photo',
              'short_description', 'main_photo', 'content', 'created_at')
    readonly_fields = ('created_at',)
    save_on_top = True

    # def get_photo(self, obj):
    #     if obj.main_photo:
    #         return mark_safe(f'<img src="{obj.main_photo.url}" width=150>')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
