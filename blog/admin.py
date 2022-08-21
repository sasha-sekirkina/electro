from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ('get_main_photo', 'title', 'is_published', 'created_at', 'views', 'category')
    list_display_links = ('title',)
    search_fields = ('title', 'short_description')
    list_editable = ('is_published',)
    list_filter = ('category', 'is_published')
    list_select_related = True
    prepopulated_fields = {'slug': ('title',)}
    fields = ('title', 'slug', 'is_published', 'category',
              'short_description', 'main_photo', 'content', 'created_at')
    readonly_fields = ('created_at',)
    save_on_top = True
    actions = ['make_published', 'make_unpublished']

    def get_main_photo(self, obj):
        if obj.main_photo:
            return mark_safe(f'<img src="{obj.main_photo.url}" width=75>')

    get_main_photo.short_description = 'Обложка'

    @admin.action(description='Опубликовать посты')
    def make_published(self, request, queryset):
        for item in queryset:
            item.is_published = True
            item.save()

    @admin.action(description='Снять посты с публикации')
    def make_unpublished(self, request, queryset):
        for item in queryset:
            item.is_published = False
            item.save()


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
