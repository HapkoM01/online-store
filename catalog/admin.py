from django.contrib import admin
from django.contrib import messages
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Настройка отображения категорий в админке"""
    list_display = ('id', 'name')
    list_display_links = ('name',)
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Настройка отображения продуктов в админке"""
    list_display = ('id', 'name', 'price', 'category', 'is_published', 'owner')
    list_display_links = ('name',)
    list_filter = ('category', 'created_at', 'is_published')
    search_fields = ('name', 'description')
    list_editable = ('price', 'is_published')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description', 'image', 'category')
        }),
        ('Цена', {
            'fields': ('price',)
        }),
        ('Публикация', {
            'fields': ('is_published', 'owner')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['make_published', 'make_unpublished']

    def make_published(self, request, queryset):
        """Массовая публикация товаров"""
        updated = queryset.update(is_published=True)
        self.message_user(request, f'{updated} товаров успешно опубликовано.', messages.SUCCESS)

    make_published.short_description = 'Опубликовать выбранные товары'

    def make_unpublished(self, request, queryset):
        """Массовое снятие с публикации товаров"""
        updated = queryset.update(is_published=False)
        self.message_user(request, f'{updated} товаров снято с публикации.', messages.WARNING)

    make_unpublished.short_description = 'Снять с публикации выбранные товары'
