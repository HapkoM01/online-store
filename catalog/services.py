from django.core.cache import cache
from django.db.models import QuerySet
from catalog.models import Product, Category
import logging

logger = logging.getLogger(__name__)


class ProductService:
    """Сервис для работы с продуктами с кешированием"""

    @staticmethod
    def get_product_detail(product_id: int) -> Product:
        """
        Получение продукта с кешированием.
        Ключ: product_detail_{id}
        TTL: 3600 секунд (1 час)
        """
        cache_key = f'product_detail_{product_id}'
        product = cache.get(cache_key)

        if product is None:
            logger.info(f'Кеш не найден для product_{product_id}, загружаем из БД')
            try:
                product = Product.objects.select_related('category', 'owner').get(id=product_id)
                cache.set(cache_key, product, timeout=3600)  # 1 час
                logger.info(f'Данные product_{product_id} сохранены в кеш')
            except Product.DoesNotExist:
                return None
        else:
            logger.info(f'Данные product_{product_id} получены из кеша')

        return product

    @staticmethod
    def get_products_by_category(category_id: int) -> QuerySet:
        """
        Получение всех продуктов в категории с кешированием.
        Ключ: category_{id}
        TTL: 1800 секунд (30 минут)
        """
        cache_key = f'category_{category_id}'
        products = cache.get(cache_key)

        if products is None:
            logger.info(f'Кеш не найден для категории {category_id}, загружаем из БД')
            try:
                category = Category.objects.get(id=category_id)
                products = Product.objects.filter(
                    category=category,
                    is_published=True
                ).select_related('category')

                # Сохраняем в кеш список ID для экономии места
                product_ids = list(products.values_list('id', flat=True))
                cache.set(cache_key, product_ids, timeout=1800)  # 30 минут
                logger.info(f'Данные категории {category_id} сохранены в кеш')

                # Сохраняем сами продукты отдельно
                for product in products:
                    ProductService.get_product_detail(product.id)

                return products
            except Category.DoesNotExist:
                return []
        else:
            logger.info(f'Данные категории {category_id} получены из кеша')
            products = Product.objects.filter(id__in=product_ids)
            return products

    @staticmethod
    def get_all_products() -> QuerySet:
        """
        Получение всех опубликованных продуктов с низкоуровневым кешированием.
        Ключ: all_products
        TTL: 600 секунд (10 минут)
        """
        cache_key = 'all_products'
        product_ids = cache.get(cache_key)

        if product_ids is None:
            logger.info('Кеш всех продуктов не найден, загружаем из БД')
            products = Product.objects.filter(is_published=True).select_related('category')
            product_ids = list(products.values_list('id', flat=True))
            cache.set(cache_key, product_ids, timeout=600)  # 10 минут
            logger.info(f'Данные всех продуктов сохранены в кеш ({len(product_ids)} записей)')

            # Кешируем каждый продукт отдельно
            for product in products:
                cache.set(f'product_detail_{product.id}', product, timeout=3600)

            return products
        else:
            logger.info('Данные всех продуктов получены из кеша')
            products = Product.objects.filter(id__in=product_ids).select_related('category')
            return products

    @staticmethod
    def clear_product_cache(product_id: int):
        """Очистка кеша для продукта"""
        cache.delete(f'product_detail_{product_id}')
        cache.delete('all_products')
        # Очищаем кеш для всех категорий
        for category in Category.objects.all():
            cache.delete(f'category_{category.id}')
        logger.info(f'Кеш очищен для product_{product_id}')

    @staticmethod
    def clear_category_cache(category_id: int):
        """Очистка кеша для категории"""
        cache.delete(f'category_{category_id}')
        cache.delete('all_products')
        logger.info(f'Кеш очищен для категории {category_id}')
