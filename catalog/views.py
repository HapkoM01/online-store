from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from catalog.models import Product, Category
from catalog.forms import ProductForm
from catalog.services import ProductService
import logging

logger = logging.getLogger(__name__)


class HomeView(ListView):
    """Главная страница с кешированием"""
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'
    extra_context = {
        'title': 'Skystore - Магазин техники 2026',
        'slogan': '🚀 Передовые технологии 2026 года уже здесь'
    }

    def get_queryset(self):
        """Получаем все опубликованные продукты с кешированием"""
        return ProductService.get_all_products()


class ProductDetailView(DetailView):
    """Детальная страница товара с кешированием"""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        """Получаем продукт через сервис с кешированием"""
        product_id = self.kwargs.get('pk')
        return ProductService.get_product_detail(product_id)


class CategoryProductsView(ListView):
    """Представление для отображения товаров в категории"""
    model = Product
    template_name = 'catalog/category_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        """Получаем товары категории через сервис с кешированием"""
        category_id = self.kwargs.get('pk')
        return ProductService.get_products_by_category(category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('pk')
        category = get_object_or_404(Category, id=category_id)
        context['category'] = category
        context['title'] = f'Товары в категории "{category.name}"'
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')
    login_url = '/users/login/'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, f'Товар "{form.instance.name}" успешно создан!')
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')
    login_url = '/users/login/'

    def test_func(self):
        product = self.get_object()
        user = self.request.user
        return product.owner == user or user.has_perm('catalog.can_unpublish_product')

    def form_valid(self, form):
        # Очищаем кеш при обновлении
        ProductService.clear_product_cache(self.object.id)
        messages.success(self.request, f'Товар "{form.instance.name}" успешно обновлен!')
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')
    login_url = '/users/login/'

    def test_func(self):
        product = self.get_object()
        user = self.request.user
        return product.owner == user or user.has_perm('catalog.can_unpublish_product')

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        product_name = product.name

        # Очищаем кеш при удалении
        ProductService.clear_product_cache(product.id)

        messages.success(self.request, f'Товар "{product_name}" успешно удален!')
        return super().delete(request, *args, **kwargs)


class ProductModerateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    fields = ['is_published']
    template_name = 'catalog/product_moderate.html'
    success_url = reverse_lazy('catalog:home')
    login_url = '/users/login/'

    def test_func(self):
        return self.request.user.has_perm('catalog.can_unpublish_product')

    def form_valid(self, form):
        # Очищаем кеш при изменении статуса публикации
        ProductService.clear_product_cache(self.object.id)
        ProductService.clear_category_cache(self.object.category.id)
        messages.success(self.request, f'Статус публикации товара "{self.object.name}" обновлен!')
        return super().form_valid(form)


class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Контакты - Skystore'
        return context

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        print(f"\n=== Получены данные из формы контактов ===")
        print(f"Имя: {name}")
        print(f"Телефон: {phone}")
        print(f"Сообщение: {message}")
        print(f"========================================\n")

        context = self.get_context_data(**kwargs)
        context['success'] = True
        context['message'] = 'Ваше сообщение отправлено! Мы свяжемся с вами в ближайшее время.'
        return self.render_to_response(context)


class Custom404View(TemplateView):
    template_name = 'catalog/404.html'


class Custom500View(TemplateView):
    template_name = 'catalog/500.html'
