from django import forms

from .models import Reviews


class ReviewForm(forms.ModelForm):
    """Форма отзыва"""
    class Meta:
        # модель
        model = Reviews
        # поля из модели для заполнения
        fields = ['name', 'email', 'text']
