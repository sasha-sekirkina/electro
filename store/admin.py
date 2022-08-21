from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Product, Producer, Category, StoreInfo


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ('get_photo','name', 'price', 'old_price', 'sale', 'is_available', 'category', 'producer')
    list_display_links = ('name', 'get_photo')
    search_fields = ('name', 'description')
    # list_editable = ()
    list_filter = ('category', 'producer', 'sale')
    fields = (
        ('name', 'price', 'sale', 'old_price'),
        ('amount', 'is_available'),
        ('slug', 'category', 'producer'),
        'description', 'characteristics', 'photo')
    list_select_related = True
    prepopulated_fields = {"slug": ("name",)}
    actions = ['make_unavailable', 'make_available',
               'increase_qty_by20', 'make_qtu_50']

    save_on_top = True
    actions = ['make_unavailable', 'make_available',
               'increase_qty_by20', 'make_qtu_50',
               'sale_20', 'sale_50', 'not_for_sale']

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width=50>')

    @admin.action(description='Нет в наличии')
    def make_unavailable(self, request, queryset):
        for item in queryset:
            item.is_available = True
            item.save()

    @admin.action(description='Есть в наличии')
    def make_available(self, request, queryset):
        for item in queryset:
            item.is_available = True
            item.save()

    @admin.action(description='В наличии + 20 штук')
    def increase_qty_by20(self, request, queryset):
        for item in queryset:
            item.amount += 20
            item.save()

    @admin.action(description='В наличии 50 штук')
    def make_qtu_50(self, request, queryset):
        for item in queryset:
            item.amount = 50
            item.save()
        # ---------------------------------------------------------------

    @admin.action(description='Скидка 20 процентов')
    def sale_20(self, request, queryset):
        for item in queryset:
            item.sale = True
            old = item.old_price
            item.price = round(((old / 100) * 80) / 100) * 100 - 1
            item.save()

    @admin.action(description='Скидка 50 процентов')
    def sale_50(self, request, queryset):
        for item in queryset:
            item.sale = True
            old = item.old_price
            item.price = round(((old / 100) * 50) / 100) * 100 - 1
            item.save()

    @admin.action(description='Нет скидки')
    def not_for_sale(self, request, queryset):
        for item in queryset:
            item.sale = False
            item.price = item.old_price
            item.save()


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
