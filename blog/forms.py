from django import forms
from blog.models import BlogPost


class BlogPostForm(forms.ModelForm):
    """Форма для блоговой записи"""

    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'preview', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите заголовок'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Введите содержимое'}),
            'preview': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
