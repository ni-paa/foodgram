"""
Фильтры для API приложения рецептов.

Этот модуль содержит классы фильтров для поиска и фильтрации
ингредиентов и рецептов по различным критериям.
"""

from django_filters import rest_framework as filters
from rest_framework.filters import BaseFilterBackend

from recipes.models import Recipe, User


class IngredientFilter(BaseFilterBackend):
    """
    Фильтр для поиска ингредиентов по имени.

    Поддерживает поиск по началу названия ингредиента.
    """

    def filter_queryset(self, request, queryset, view):
        """Метод для поиска ингредиентов по указанному имени."""
        if 'name' in request.query_params:
            # Фильтруем по началу названия
            queryset = queryset.filter(
                name__startswith=request.query_params['name']
            )
        return queryset


class RecipeFilter(filters.FilterSet):
    """
    Фильтр для рецептов.

    Позволяет фильтровать рецепты по автору, тегам,
    избранному и списку покупок.
    """

    # Фильтр по автору рецепта
    author = filters.ModelChoiceFilter(queryset=User.objects.all())

    # Фильтр по тегам
    tags = filters.CharFilter(method='filter_tags')

    # Фильтр по избранному
    is_favorited = filters.BooleanFilter(
        method='filter_is_favorited'
    )

    # Фильтр по списку покупок
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author',)

    def filter_tags(self, recipes, name, value):
        """Фильтрация рецептов по списку тегов (slug)."""
        tags = self.request.query_params.getlist('tags')
        if tags:
            # Фильтруем рецепты, содержащие хотя бы один из тегов
            return recipes.filter(tags__slug__in=tags).distinct()
        return recipes

    def filter_is_favorited(self, recipes, name, value):
        """Фильтрация рецептов по избранному текущего пользователя."""
        user = self.request.user
        if not user.is_authenticated:
            return recipes

        # Если value=True, показываем только избранные
        # Если value=False, исключаем избранные
        return recipes.filter(
            favorites__user=user) if value else recipes.exclude(
                favorites__user=user)

    def filter_is_in_shopping_cart(self, recipes, name, value):
        """Фильтрация рецептов по списку покупок текущего пользователя."""
        user = self.request.user
        if not user.is_authenticated:
            return recipes

        # Аналогично избранному
        return recipes.filter(
            shoppingcarts__user=user) if value else recipes.exclude(
                shoppingcarts__user=user)
