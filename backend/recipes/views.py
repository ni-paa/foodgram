from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect

from .models import Recipe


def recipe_redirect(request, pk):
    recipe = get_object_or_404(Recipe, id=pk)
    return redirect(recipe.get_absolute_url())


def index_view(request):
    return HttpResponse("<h1>Foodgram Backend</h1><p>Backend работает успешно! 🎉</p><p>Для работы с фронтендом, запустите React приложение из директории <code>frontend/</code>.</p><p>Документация API: <a href='/docs/'>/docs/</a></p><p>Админ панель: <a href='/admin/'>/admin/</a></p>")
