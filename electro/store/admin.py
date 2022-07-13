from django.contrib import admin

from .models import Product, Producer, Category


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ('id', 'name', 'price', 'is_available', 'amount', 'category', 'producer')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'description')
    list_editable = ('amount',)
    list_filter = ('is_available', 'category', 'producer')
    fields = (('name', 'price'), ('is_available', 'amount'), ('slug', 'category', 'producer'), 'description', 'photo')
    list_select_related = True
    prepopulated_fields = {"slug": ("name",)}

    save_on_top = True

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


admin.site.register(Product, ProductAdmin)
admin.site.register(Producer, ProducerAdmin)
admin.site.register(Category, CategoryAdmin)
