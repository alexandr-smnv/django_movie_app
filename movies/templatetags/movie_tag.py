from django import template
from movies.models import Category, Movie

# Создание экземпляра Library для регистрации templatetags
register = template.Library()


# декоратор регистрирует функцию как templatetag
@register.simple_tag()
def get_categories():
    """Вывод всех категорий"""
    return Category.objects.all()


@register.inclusion_tag('movies/tags/last_movie.html')
def get_last_movies(count=5):
    # Сортировка по id
    movies = Movie.objects.order_by('id')[:count]
    return {'last_movies': movies}
