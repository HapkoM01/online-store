from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
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

        # Дополнительное задание: отправка поздравления при 100 просмотрах
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
                recipient_list=['your-email@example.com'],  # Замените на ваш email
                fail_silently=True,
            )
            print(f"Поздравление отправлено для статьи '{post.title}'")
        except Exception as e:
            print(f"Ошибка отправки email: {e}")


class BlogCreateView(CreateView):
    """Создание новой блоговой записи"""
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/blog_form.html'
    success_url = reverse_lazy('blog:blog_list')


class BlogUpdateView(UpdateView):
    """Редактирование блоговой записи"""
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/blog_form.html'

    def get_success_url(self):
        """После успешного редактирования перенаправляем на страницу статьи"""
        return reverse_lazy('blog:blog_detail', args=[self.object.id])


class BlogDeleteView(DeleteView):
    """Удаление блоговой записи"""
    model = BlogPost
    template_name = 'blog/blog_confirm_delete.html'
    success_url = reverse_lazy('blog:blog_list')
