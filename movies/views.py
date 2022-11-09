from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django.views.generic import ListView, DetailView

from movies.forms import ReviewForm
from movies.models import Movie


class MoviesView(ListView):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.all().filter(draft=False)


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
            # внесение изменений в форму (связываем комментарий с фильмом)
            form.movie = movie
            # сохранение формы
            form.save()
        return redirect(movie.get_absolute_url())
