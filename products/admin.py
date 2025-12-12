from django.contrib import admin
from .models import Product, Category
from django.utils.html import format_html

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category', 'thumbnail')
    readonly_fields = ('preview',)
    list_filter = ('category',)
    search_fields = ('name',)

    def thumbnail(self, obj):
        if obj.image:
            return format_html(f'<img src="{obj.image.url}" width="50" />')
        return "-"
    thumbnail.short_description = "Image"

    def preview(self, obj):
        if obj.image:
            return format_html(f'<img src="{obj.image.url}" width="200" />')
        return "No Image"