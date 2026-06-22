from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.conf import settings
from blog.models import BlogPost
from blog.forms import BlogPostForm


class BlogListView(ListView):
    """Список блоговых записей (только опубликованные)"""
    model = BlogPost
    template_name = 'blog/blog_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        """Выводим только опубликованные статьи"""
        return BlogPost.objects.filter(is_published=True)


class BlogDetailView(DetailView):
    """Детальная страница блоговой записи с увеличением счетчика просмотров"""
    model = BlogPost
    template_name = 'blog/blog_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        """Переопределяем метод get_object для увеличения счетчика просмотров"""
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save()

        # Отправка поздравления при 100 просмотрах
        if obj.views_count == 100:
            self.send_congratulation_email(obj)

        return obj

    def send_congratulation_email(self, post):
        """Отправляет поздравление на почту при достижении 100 просмотров"""
        try:
            send_mail(
                subject=f'🎉 Поздравление! Статья "{post.title}" набрала 100 просмотров!',
                message=f'Ваша статья "{post.title}" достигла 100 просмотров.\n\n'
                        f'Ссылка: http://127.0.0.1:8000/blogs/{post.id}/\n\n'
                        f'Продолжайте в том же духе! 🚀',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['your-email@example.com'],
                fail_silently=True,
            )
            print(f"Поздравление отправлено для статьи '{post.title}'")
        except Exception as e:
            print(f"Ошибка отправки email: {e}")


class BlogCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Создание новой блоговой записи (только для контент-менеджеров)"""
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/blog_form.html'
    success_url = reverse_lazy('blog:blog_list')
    login_url = '/users/login/'

    def test_func(self):
        """Проверка права на создание блоговой записи"""
        return self.request.user.has_perm('blog.add_blogpost')

    def handle_no_permission(self):
        """Обработка отсутствия прав"""
        messages.error(self.request, 'У вас нет прав для создания статей в блоге. Только контент-менеджеры могут создавать статьи.')
        return super().handle_no_permission()

    def form_valid(self, form):
        messages.success(self.request, f'Статья "{form.instance.title}" успешно создана!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)


class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Редактирование блоговой записи (только для контент-менеджеров)"""
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/blog_form.html'
    login_url = '/users/login/'

    def test_func(self):
        """Проверка права на изменение блоговой записи"""
        return self.request.user.has_perm('blog.change_blogpost')

    def handle_no_permission(self):
        """Обработка отсутствия прав"""
        messages.error(self.request, 'У вас нет прав для редактирования статей в блоге. Только контент-менеджеры могут редактировать статьи.')
        return super().handle_no_permission()

    def get_success_url(self):
        """После успешного редактирования перенаправляем на страницу статьи"""
        return reverse_lazy('blog:blog_detail', args=[self.object.id])

    def form_valid(self, form):
        messages.success(self.request, f'Статья "{form.instance.title}" успешно обновлена!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)


class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление блоговой записи (только для контент-менеджеров)"""
    model = BlogPost
    template_name = 'blog/blog_confirm_delete.html'
    success_url = reverse_lazy('blog:blog_list')
    login_url = '/users/login/'

    def test_func(self):
        """Проверка права на удаление блоговой записи"""
        return self.request.user.has_perm('blog.delete_blogpost')

    def handle_no_permission(self):
        """Обработка отсутствия прав"""
        messages.error(self.request, 'У вас нет прав для удаления статей в блоге. Только контент-менеджеры могут удалять статьи.')
        return super().handle_no_permission()

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, f'Статья "{self.get_object().title}" успешно удалена!')
        return super().delete(request, *args, **kwargs)
