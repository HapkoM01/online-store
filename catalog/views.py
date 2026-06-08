from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from catalog.models import Product, Category
from catalog.forms import ProductForm


class HomeView(ListView):
    """Контроллер для главной страницы (список товаров)"""
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'
    extra_context = {
        'title': 'Skystore - Магазин техники 2026',
        'slogan': '🚀 Передовые технологии 2026 года уже здесь'
    }

    def get_queryset(self):
        """Получаем все продукты"""
        return Product.objects.all()


class ProductDetailView(DetailView):
    """Контроллер для страницы товара"""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(CreateView):
    """Контроллер для создания продукта"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        """Дополнительные действия при успешной валидации"""
        messages.success(self.request, f'Товар "{form.instance.name}" успешно создан!')
        return super().form_valid(form)

    def form_invalid(self, form):
        """Обработка неверной формы"""
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)


class ProductUpdateView(UpdateView):
    """Контроллер для редактирования продукта"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        messages.success(self.request, f'Товар "{form.instance.name}" успешно обновлен!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)


class ProductDeleteView(DeleteView):
    """Контроллер для удаления продукта"""
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, f'Товар "{self.get_object().name}" успешно удален!')
        return super().delete(request, *args, **kwargs)


class ContactsView(TemplateView):
    """Контроллер для страницы контактов"""
    template_name = 'catalog/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Контакты - Skystore'
        return context

    def post(self, request, *args, **kwargs):
        """Обработка POST-запроса из формы"""
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
    """Кастомная страница 404"""
    template_name = 'catalog/404.html'


class Custom500View(TemplateView):
    """Кастомная страница 500"""
    template_name = 'catalog/500.html'
