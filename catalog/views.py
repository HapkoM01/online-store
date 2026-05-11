from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings


def home(request):
    """Контроллер для главной страницы"""
    context = {
        'title': 'Skystore - Магазин плагинов и кода',
        'products': [
            {
                'name': 'Удобный сервис рассылок',
                'price': 140,
                'description': 'Неограниченная лицензия, поддержка, установка на сервер, получение обновлений'
            },
            {
                'name': 'Телеграм бот для магазина',
                'price': 200,
                'description': 'Автоматизация продаж, уведомления, поддержка клиентов'
            },
            {
                'name': 'Полезные утилиты для разработки',
                'price': 99,
                'description': 'Набор инструментов для ускорения разработки'
            },
            {
                'name': 'Веб-приложение на Django',
                'price': 350,
                'description': 'Готовый шаблон для интернет-магазина'
            }
        ]
    }
    return render(request, 'catalog/home.html', context)


def contacts(request):
    """Контроллер для страницы контактов"""
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Выводим в консоль (для проверки)
        print(f"\n=== Получены данные из формы контактов ===")
        print(f"Имя: {name}")
        print(f"Телефон: {phone}")
        print(f"Сообщение: {message}")
        print(f"========================================\n")

        # Здесь можно добавить отправку email
        # send_mail(
        #     f'Сообщение от {name}',
        #     f'Телефон: {phone}\nСообщение: {message}',
        #     settings.DEFAULT_FROM_EMAIL,
        #     ['admin@example.com'],
        #     fail_silently=False,
        # )

        context = {
            'success': True,
            'message': 'Ваше сообщение отправлено! Мы свяжемся с вами в ближайшее время.'
        }
        return render(request, 'catalog/contacts.html', context)

    return render(request, 'catalog/contacts.html')

def custom_404(request, exception):
    return render(request, 'catalog/404.html', status=404)

def custom_500(request):
    return render(request, 'catalog/500.html', status=500)
