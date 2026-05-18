from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Настройка отображения категорий в админке"""
    list_display = ('id', 'name')
    list_display_links = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)} if hasattr(Category, 'slug') else {}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Настройка отображения продуктов в админке"""
    list_display = ('id', 'name', 'price', 'category')
    list_display_links = ('name',)
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('price',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description', 'image', 'category')
        }),
        ('Цена', {
            'fields': ('price',)
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
