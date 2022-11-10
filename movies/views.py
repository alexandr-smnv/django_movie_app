from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django.views.generic import ListView, DetailView

from movies.forms import ReviewForm
from movies.models import Movie, Category


class MoviesView(ListView):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.all().filter(draft=False)

    # def get_context_data(self, *args, **kwargs):
    #     # получаем словарь контекста
    #     context = super().get_context_data(*args, **kwargs)
    #     # добавляем в контекст новое поле
    #     context['categories'] = Category.objects.all()
    #     return context


class MovieDetail(DetailView):
    """Полное описание фильма"""
    model = Movie
    # по какому полю надо искать запись
    slug_field = 'url'


class AddReview(View):
    """Отзывы"""
    def post(self, request, pk):
        # заполнение формы данными из запроса
        form = ReviewForm(request.POST)
        # к какому фильму привязывается отзыв
        movie = Movie.objects.get(id=pk)
        # проверка на валидность
        if form.is_valid():
            # приостановление сохранения формы
            form = form.save(commit=False)
            # ищем в пост запросе ключ 'parent'
            if request.POST.get('parent', None):
                #
                form.parent_id = int(request.POST.get('parent'))
            # внесение изменений в форму (связываем комментарий с фильмом)
            form.movie = movie
            # сохранение формы
            form.save()
        return redirect(movie.get_absolute_url())
