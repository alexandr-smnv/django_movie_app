from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *

# Register your models here.


from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категории"""
    # Отображаемые поля
    list_display = ("id", "name", "url")
    # Поле ссылки на объект
    list_display_links = ("name",)


class ReviewInline(admin.TabularInline):
    """Отзывы на странице фильма"""
    # Модель
    model = Reviews
    # Количество объектов
    extra = 1
    # Поля только для чтения
    readonly_fields = ("name", "email")


class MovieShotsInline(admin.TabularInline):
    # Модель
    model = MovieShots
    # Количество объектов
    extra = 1
    # Поля только для чтения
    readonly_fields = ("get_image",)

    # Миниатюра изображения
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="110"')

    # Название столбца
    get_image.short_description = "Изображение"


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Фильмы"""
    # Отображаемые поля
    list_display = ("title", "category", "url", "draft")
    # Фильтрация по полям
    list_filter = ("category", "year")
    # Поиск по полям
    search_fields = ("title", "category__name")
    # Отображение связанного объекта
    inlines = [MovieShotsInline, ReviewInline]
    # Кнопки "Сохранить" отображаются и сверху
    save_on_top = True
    # Добавление кнопки "Сохранить как новый объект"
    save_as = True
    # Регистрация формы skeditor
    form = MovieAdminForm
    # Редактирование в списке объектов
    list_editable = ("draft",)
    # Поля только для чтения
    readonly_fields = ("get_image",)
    # Группировка полей
    fieldsets = (
        (None, {
            "fields": (("title", "tagline"),)
        }),
        (None, {
            "fields": ("description", ("poster", "get_image"))
        }),
        (None, {
            "fields": (("year", "world_premiere", "country"),)

        }),
        ("Actors", {
            "classes": ("collapse",),
            "fields": (("actors", "directors", "genres", "category"),)
        }),
        (None, {
            "fields": (("budget", "fees_in_usa", "fees_in_world"),)
        }),
        ("Options", {
            "fields": (("url", "draft"),)
        }),
    )

    # Миниатюра изображения
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="100" height="110"')
    # Название столбца
    get_image.short_description = "Постер"


@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    """Отзывы"""
    # Отображаемые поля
    list_display = ("name", "email", "parent", "movie", "id")
    # Поля только для чтения
    readonly_fields = ("name", "email")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Жанры"""
    # Отображаемые поля
    list_display = ("name", "url")


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """Актеры"""
    # Отображаемые поля
    list_display = ("name", "age", "get_image")
    # Поля только для чтения
    readonly_fields = ("get_image",)

    # Миниатюра изображения
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    # Название столбца
    get_image.short_description = "Изображение"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    # Отображаемые поля
    list_display = ("star", 'movie', "ip")


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    """Кадры из фильма"""
    # Отображаемые поля
    list_display = ("title", "movie", "get_image")
    # Поля только для чтения
    readonly_fields = ("get_image",)

    # Миниатюра изображения
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')
    # Название столбца
    get_image.short_description = "Изображение"


admin.site.register(RatingStar)

# Изменение заголовка админ панели
admin.site.site_title = "Django Movies"
admin.site.site_header = "Django Movies"
