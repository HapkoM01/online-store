from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.views import View
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from catalog.models import Product


class HomeView(ListView):
    """Контроллер для главной страницы (список товаров)"""
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        """Получаем все продукты"""
        return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Skystore - Магазин техники 2026'
        context['slogan'] = '🚀 Передовые технологии 2026 года уже здесь'
        return context


class ProductDetailView(DetailView):
    """Контроллер для страницы товара"""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


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

        # Выводим в консоль
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
