from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import (FavoriteRecipe, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Tag,)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug',)
    list_filter = ('name', 'color', 'slug',)
    search_fields = ('name',)
    ordering = ('name',)


class IngredientResource(resources.ModelResource):
    class Meta:
        model = Ingredient


@admin.register(Ingredient)
class IngredientAdmin(ImportExportModelAdmin):
    resource_classes = [IngredientResource]
    list_display = ('id', 'name', 'measurement_unit',)
    list_filter = ('name',)
    search_fields = ('name',)
    ordering = ('id',)


class IngredientsInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientsInline]
    list_display = ('id', 'name', 'author', 'amount_favorites',)
    search_fields = ('name', 'author',)
    list_filter = ('author', 'name', 'tags',)
    readonly_fields = ('author', 'amount_favorites')

    @admin.display(description='Количество рецептов в избранном')
    def amount_favorites(self, obj):
        return obj.favorite.count()


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'amount',)
    search_fields = ('recipe', 'ingredient',)


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    search_fields = ('user',)
