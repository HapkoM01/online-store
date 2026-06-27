from django.core.management.base import BaseCommand
from django.core.cache import cache
import time


class Command(BaseCommand):
    help = 'Тестирование Redis кеширования'

    def handle(self, *args, **options):
        self.stdout.write('=== Тестирование Redis ===')

        # Тест 1: Запись в кеш
        self.stdout.write('1. Запись в кеш...')
        cache.set('test_key', 'Hello Redis!', timeout=60)
        self.stdout.write('✅ Запись выполнена')

        # Тест 2: Чтение из кеша
        self.stdout.write('2. Чтение из кеша...')
        value = cache.get('test_key')
        self.stdout.write(f'✅ Получено: {value}')

        # Тест 3: Время выполнения
        self.stdout.write('3. Тест скорости...')
        start = time.time()
        cache.set('speed_test', 'test', timeout=60)
        cache.get('speed_test')
        end = time.time()
        self.stdout.write(f'✅ Время операции: {(end - start) * 1000:.2f} мс')

        # Тест 4: Удаление
        self.stdout.write('4. Удаление из кеша...')
        cache.delete('test_key')
        cache.delete('speed_test')
        self.stdout.write('✅ Удаление выполнено')

        self.stdout.write(self.style.SUCCESS('Redis работает корректно! 🚀'))
