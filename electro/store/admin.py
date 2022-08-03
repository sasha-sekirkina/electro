from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Product, Producer, Category, StoreInfo


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ('get_photo', 'id', 'name', 'price', 'sale', 'is_available', 'category', 'producer')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'description')
    list_editable = ('price', 'sale')
    list_filter = ('category', 'producer', 'sale')
    fields = (
        ('name', 'price', 'sale', 'old_price'),
        ('amount', 'is_available'),
        ('slug', 'category', 'producer'),
        'description', 'characteristics', 'photo')
    list_select_related = True
    prepopulated_fields = {"slug": ("name",)}

    save_on_top = True

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width=50>')


class ProducerAdmin(admin.ModelAdmin):
    model = Producer
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    prepopulated_fields = {"slug": ("name",)}


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    prepopulated_fields = {"slug": ("name",)}


class StoreInfoAdmin(admin.ModelAdmin):
    model = StoreInfo
    list_display = ('name',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Producer, ProducerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(StoreInfo, StoreInfoAdmin)
