from django.shortcuts import render, get_object_or_404
from catalog.models import Category, Product


def home(request):
    """Контроллер для главной страницы"""
    products = Product.objects.all()  # Получаем все продукты
    context = {
        'title': 'Skystore - Магазин плагинов и кода',
        'products': products
    }
    return render(request, 'catalog/home.html', context)


def product_detail(request, pk):
    """Контроллер для страницы подробной информации о товаре"""
    product = get_object_or_404(Product, pk=pk)
    context = {
        'title': product.name,
        'product': product
    }
    return render(request, 'catalog/product_detail.html', context)


def contacts(request):
    """Контроллер для страницы контактов"""
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        print(f"\n=== Получены данные из формы контактов ===")
        print(f"Имя: {name}")
        print(f"Телефон: {phone}")
        print(f"Сообщение: {message}")
        print(f"========================================\n")

        context = {
            'success': True,
            'message': 'Ваше сообщение отправлено! Мы свяжемся с вами в ближайшее время.'
        }
        return render(request, 'catalog/contacts.html', context)

    return render(request, 'catalog/contacts.html')


def custom_404(request, exception):
    """Кастомная страница 404"""
    return render(request, 'catalog/404.html', status=404)


def custom_500(request):
    """Кастомная страница 500"""
    return render(request, 'catalog/500.html', status=500)
