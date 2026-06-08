from django import forms
from django.core.exceptions import ValidationError
from catalog.models import Product
from PIL import Image

# Список запрещенных слов
FORBIDDEN_WORDS = [
    'казино', 'криптовалюта', 'крипта', 'биржа',
    'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
]


class ProductForm(forms.ModelForm):
    """Форма для создания и редактирования продукта"""

    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Стилизация полей (Задание 3)
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите название товара'
        })
        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Введите описание товара'
        })
        self.fields['image'].widget.attrs.update({
            'class': 'form-control',
            'accept': 'image/jpeg,image/png'
        })
        self.fields['category'].widget.attrs.update({
            'class': 'form-select'
        })
        self.fields['price'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите цену товара',
            'step': '0.01',
            'min': '0'
        })

    def clean_name(self):
        """Валидация названия продукта (запрещенные слова)"""
        name = self.cleaned_data.get('name')
        if name:
            name_lower = name.lower()
            for forbidden_word in FORBIDDEN_WORDS:
                if forbidden_word in name_lower:
                    raise ValidationError(
                        f'Название не может содержать слово "{forbidden_word}". '
                        f'Пожалуйста, удалите запрещенное слово.'
                    )
        return name

    def clean_description(self):
        """Валидация описания продукта (запрещенные слова)"""
        description = self.cleaned_data.get('description')
        if description:
            description_lower = description.lower()
            forbidden_found = []
            for forbidden_word in FORBIDDEN_WORDS:
                if forbidden_word in description_lower:
                    forbidden_found.append(forbidden_word)

            if forbidden_found:
                words = ', '.join(forbidden_found)
                raise ValidationError(
                    f'Описание содержит запрещенные слова: {words}. '
                    f'Пожалуйста, удалите их.'
                )
        return description

    def clean_price(self):
        """Валидация цены продукта (не может быть отрицательной)"""
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise ValidationError(
                'Цена продукта не может быть отрицательной. '
                'Пожалуйста, введите корректную цену.'
            )
        return price


class ProductDeleteForm(forms.Form):
    """Форма для подтверждения удаления продукта"""
    confirm = forms.BooleanField(
        required=True,
        label='Подтверждаю удаление',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )


def clean_image(self):
    """Валидация изображения (формат и размер)"""
    image = self.cleaned_data.get('image')

    if image:
        # Проверка размера файла (максимум 5 МБ = 5 * 1024 * 1024 байт)
        max_size = 5 * 1024 * 1024  # 5 MB
        if image.size > max_size:
            raise ValidationError(
                f'Размер изображения не должен превышать 5 МБ. '
                f'Текущий размер: {image.size // (1024 * 1024)} МБ'
            )

        # Проверка формата файла
        allowed_formats = ['JPEG', 'PNG']
        try:
            img = Image.open(image)
            if img.format not in allowed_formats:
                raise ValidationError(
                    f'Неподдерживаемый формат изображения. '
                    f'Разрешены форматы: {", ".join(allowed_formats)}'
                )
        except Exception:
            raise ValidationError('Файл не является корректным изображением.')

    return image
