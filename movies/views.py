from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django.views.generic import ListView, DetailView

from movies.forms import ReviewForm, RatingForm
from movies.models import Movie, Category, Actor, Genre, Rating


class GenreYear:
    """Жанры и года выхода фильмов"""

    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values('year')


class MoviesView(GenreYear, ListView):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.all().filter(draft=False)
    paginate_by = 3


class MovieDetail(GenreYear, DetailView):
    """Полное описание фильма"""
    model = Movie
    # по какому полю надо искать запись
    slug_field = 'url'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # добавляем ключ star_form и значение заносим в форму
        context['star_form'] = RatingForm()
        context['form'] = ReviewForm()
        return context


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


class ActorView(GenreYear, DetailView):
    """Вывод информации об актере"""
    model = Actor
    template_name = 'movies/actor.html'
    # поле по которому будем искать актеров
    slug_field = 'name'


class FilterMoviesView(GenreYear, ListView):
    """Фильтр фильмов"""
    paginate_by = 2

    def get_queryset(self):
        # фильмы будут фильтроваться по значению годов, которые будут
        # входить в список возвращаемый из фронта
        # с помощью getlist мы будем доставать все значения годов
        queryset = Movie.objects.filter(
            # Q используется для того чтобы можно было запрашивать или года
            # или жанры или все вместе
            Q(year__in=self.request.GET.getlist('year')) |
            Q(genres__in=self.request.GET.getlist('genre'))
        ).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['year'] = ''.join([f'year={x}&' for x in self.request.GET.getlist('year')])
        context['genre'] = ''.join([f'genre={x}&' for x in self.request.GET.getlist('genre')])
        return context


class AddStarRating(View):
    """Добавление рейтинга фильму"""

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get("movie")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


class Search(ListView):
    """Поиск фильмов"""
    paginate_by = 3

    def get_queryset(self):
        # Фильтруем фильмы по названию (icontains - не учитывая регистр)
        # И сравниваем с параметрами в GET
        return Movie.objects.filter(title__icontains=self.request.GET.get("q"))

    #
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['q'] = f'q={self.request.GET.get("q")}&'
        return context
