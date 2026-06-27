from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm
from .models import User


class UserRegistrationView(CreateView):
    """Представление для регистрации пользователя"""
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """Отправка приветственного письма после успешной регистрации"""
        response = super().form_valid(form)

        # Отправка приветственного письма
        try:
            send_mail(
                subject='Добро пожаловать в SkyStore!',
                message=f'''
                Здравствуйте, {form.cleaned_data.get('first_name')}!

                Благодарим вас за регистрацию в интернет-магазине SkyStore.

                Ваши данные для входа:
                Email: {form.cleaned_data.get('email')}

                Теперь вы можете просматривать каталог, оставлять отзывы и управлять своими товарами.

                С уважением,
                Команда SkyStore
                ''',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[form.cleaned_data.get('email')],
                fail_silently=False,
            )
            messages.success(self.request, 'Регистрация прошла успешно! Проверьте вашу почту.')
        except Exception as e:
            messages.warning(self.request, 'Регистрация прошла успешно, но письмо не было отправлено.')

        return response

    def form_invalid(self, form):
        """Обработка неверной формы"""
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'{error}')
        return super().form_invalid(form)


class UserLoginView(LoginView):
    """Представление для авторизации пользователя"""
    form_class = UserLoginForm
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('catalog:home')

    def form_valid(self, form):
        messages.success(self.request, f'Добро пожаловать, {form.user_cache.get_full_name() or form.user_cache.email}!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Неверный email или пароль. Попробуйте снова.')
        return super().form_invalid(form)


@login_required
def user_logout(request):
    """Выход из системы"""
    logout(request)
    messages.info(request, 'Вы успешно вышли из системы.')
    return redirect('catalog:home')


class UserProfileUpdateView(UpdateView):
    """Представление для редактирования профиля пользователя (доп. задание)"""
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def form_valid(self, form):
        messages.success(self.request, 'Ваш профиль успешно обновлен!')
        return super().form_valid(form)
