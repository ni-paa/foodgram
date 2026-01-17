from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView

from .models import Recipe


def recipe_redirect(request, pk):
    recipe = get_object_or_404(Recipe, id=pk)
    return redirect(recipe.get_absolute_url())


class IndexView(TemplateView):
    template_name = 'index.html'
