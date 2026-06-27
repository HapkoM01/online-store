from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Настройка отображения кастомной модели пользователя в админке"""

    # Поля для отображения в списке
    list_display = ('id', 'email', 'first_name', 'last_name', 'phone_number', 'country', 'is_active', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'country', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name', 'phone_number')

    # Поля для отображения на странице редактирования
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'avatar', 'phone_number', 'country')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    # Поля для создания нового пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone_number', 'country', 'password1', 'password2'),
        }),
    )

    # Поля для упорядочивания
    ordering = ('email',)
