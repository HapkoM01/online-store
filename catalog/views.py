from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from catalog.models import Product, Category
from catalog.forms import ProductForm


class HomeView(ListView):
    """Главная страница - показываем только опубликованные продукты"""
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'
    extra_context = {
        'title': 'Skystore - Магазин техники 2026',
        'slogan': '🚀 Передовые технологии 2026 года уже здесь'
    }

    def get_queryset(self):
        """Показываем только опубликованные продукты"""
        return Product.objects.filter(is_published=True)


class ProductDetailView(DetailView):
    """Детальная страница товара"""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Создание продукта (только для авторизованных)"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')
    login_url = '/users/login/'

    def form_valid(self, form):
        """Автоматически назначаем владельца"""
        form.instance.owner = self.request.user
        # Новый продукт по умолчанию не опубликован (is_published=False)
        messages.success(self.request, f'Товар "{form.instance.name}" успешно создан! Он ожидает модерации.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Редактирование продукта (только владелец или модератор)"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')
    login_url = '/users/login/'

    def test_func(self):
        """Проверка прав: владелец или модератор"""
        product = self.get_object()
        user = self.request.user

        # Владелец может редактировать
        if product.owner == user:
            return True

        # Модератор может редактировать
        if user.has_perm('catalog.can_unpublish_product'):
            return True

        return False

    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав для редактирования этого товара.')
        return redirect('catalog:home')

    def form_valid(self, form):
        messages.success(self.request, f'Товар "{form.instance.name}" успешно обновлен!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление продукта (владелец или модератор)"""
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')
    login_url = '/users/login/'

    def test_func(self):
        """Проверка прав: владелец или модератор"""
        product = self.get_object()
        user = self.request.user

        # Владелец может удалить
        if product.owner == user:
            return True

        # Модератор может удалить
        if user.has_perm('catalog.can_unpublish_product'):
            return True

        return False

    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав для удаления этого товара.')
        return redirect('catalog:home')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, f'Товар "{self.get_object().name}" успешно удален!')
        return super().delete(request, *args, **kwargs)


class ProductModerateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Представление для модерации продукта (публикация/снятие с публикации)"""
    model = Product
    fields = ['is_published']
    template_name = 'catalog/product_moderate.html'
    success_url = reverse_lazy('catalog:home')
    login_url = '/users/login/'

    def test_func(self):
        """Только модераторы могут управлять публикацией"""
        return self.request.user.has_perm('catalog.can_unpublish_product')

    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав для модерации товаров.')
        return redirect('catalog:home')


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