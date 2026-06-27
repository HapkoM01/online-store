from django.test import TestCase
from django.urls import reverse


class CatalogViewsTest(TestCase):
    """Тесты для контроллеров приложения catalog"""

    def test_home_page_status_code(self):
        """Проверка, что главная страница загружается"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_page_uses_correct_template(self):
        """Проверка, что главная страница использует правильный шаблон"""
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'catalog/home.html')

    def test_contacts_page_status_code(self):
        """Проверка, что страница контактов загружается"""
        response = self.client.get('/contacts/')
        self.assertEqual(response.status_code, 200)

    def test_contacts_page_uses_correct_template(self):
        """Проверка, что страница контактов использует правильный шаблон"""
        response = self.client.get('/contacts/')
        self.assertTemplateUsed(response, 'catalog/contacts.html')

    def test_contacts_post_request(self):
        """Проверка POST-запроса к странице контактов"""
        response = self.client.post('/contacts/', {
            'name': 'Тестовый пользователь',
            'phone': '+7 (999) 123-45-67',
            'message': 'Тестовое сообщение'
        })
        self.assertEqual(response.status_code, 200)

    def test_404_page(self):
        """Проверка, что несуществующая страница возвращает 404"""
        response = self.client.get('/nonexistent-page/')
        self.assertEqual(response.status_code, 404)


class CatalogUrlsTest(TestCase):
    """Тесты для URL-маршрутов"""

    def test_home_url_reverse(self):
        """Проверка обратного разрешения URL для главной страницы"""
        url = reverse('catalog:home')
        self.assertEqual(url, '/')

    def test_contacts_url_reverse(self):
        """Проверка обратного разрешения URL для страницы контактов"""
        url = reverse('catalog:contacts')
        self.assertEqual(url, '/contacts/')
