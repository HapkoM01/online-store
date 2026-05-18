import os
import json
from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Category, Product
from django.conf import settings


class Command(BaseCommand):
    help = 'Загрузка тестовых данных из фикстур'

    def handle(self, *args, **options):
        self.stdout.write('Начинаем загрузку тестовых данных...')

        # Удаляем существующие данные
        self.stdout.write('Очищаем существующие данные...')
        Category.objects.all().delete()
        Product.objects.all().delete()

        # Путь к фикстурам
        fixtures_dir = os.path.join(settings.BASE_DIR, 'catalog', 'fixtures')

        # Загружаем категории
        categories_file = os.path.join(fixtures_dir, 'categories.json')
        if os.path.exists(categories_file):
            self.stdout.write('Загружаем категории...')
            call_command('loaddata', categories_file)
        else:
            self.stdout.write('Файл categories.json не найден, создаем тестовые категории...')
            self.create_test_categories()

        # Загружаем продукты
        products_file = os.path.join(fixtures_dir, 'products.json')
        if os.path.exists(products_file):
            self.stdout.write('Загружаем продукты...')
            call_command('loaddata', products_file)
        else:
            self.stdout.write('Файл products.json не найден, создаем тестовые продукты...')
            self.create_test_products()

        self.stdout.write(
            self.style.SUCCESS(
                f'Загрузка завершена! Добавлено категорий: {Category.objects.count()}, '
                f'продуктов: {Product.objects.count()}'
            )
        )

    def create_test_categories(self):
        """Создание тестовых категорий"""
        categories_data = [
            {'name': 'Электроника', 'description': 'Смартфоны, ноутбуки, планшеты'},
            {'name': 'Одежда', 'description': 'Мужская и женская одежда'},
            {'name': 'Книги', 'description': 'Художественная и учебная литература'},
            {'name': 'Дом и сад', 'description': 'Товары для дома и дачи'},
        ]

        for cat_data in categories_data:
            Category.objects.create(**cat_data)

    def create_test_products(self):
        """Создание тестовых продуктов"""
        electronics = Category.objects.get(name='Электроника')
        clothing = Category.objects.get(name='Одежда')
        books = Category.objects.get(name='Книги')

        products_data = [
            {'name': 'iPhone 15', 'description': 'Смартфон Apple', 'price': 99900, 'category': electronics},
            {'name': 'MacBook Pro', 'description': 'Ноутбук Apple', 'price': 199900, 'category': electronics},
            {'name': 'Футболка хлопковая', 'description': 'Белая футболка', 'price': 1500, 'category': clothing},
            {'name': 'Джинсы', 'description': 'Синие джинсы', 'price': 3500, 'category': clothing},
            {'name': 'Python для начинающих', 'description': 'Учебник по Python', 'price': 1200, 'category': books},
        ]

        for prod_data in products_data:
            Product.objects.create(**prod_data)
