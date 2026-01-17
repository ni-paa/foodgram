"""
Утилиты для API приложения рецептов.

Этот модуль содержит вспомогательные функции и классы,
такие как обработка изображений в формате Base64 и генерация
отчета списка покупок.
"""

import base64
from datetime import datetime

from django.core.files.base import ContentFile
from rest_framework import serializers

from recipes.constants import (
    INGREDIENT_FORMAT, SHOPPING_LIST_HEADER, MONTH_NAMES
)


class CustomImageField(serializers.ImageField):
    """
    Кастомный класс для обработки изображений в формате Base64.

    Преобразует base64 строку в файл ContentFile для сохранения в Django.
    """

    def to_internal_value(self, data):
        """Обработка данных в формате base64."""
        if isinstance(data, str) and data.startswith('data:image'):
            try:
                # Разделяем строку на формат и данные
                format_str, imgstr = data.split(';base64,')
                # Получаем расширение файла
                ext = format_str.split('/')[-1]
                # Декодируем base64 и создаем ContentFile
                data = ContentFile(
                    base64.b64decode(imgstr), name='temp.' + ext)
            except (ValueError, TypeError):
                raise serializers.ValidationError(
                    "Неверный формат данных изображения base64"
                )
        return super().to_internal_value(data)


def generate_shopping_list_report(user, ingredients, recipes):
    """
    Создание отчета списка покупок для загрузки.

    Формирует текстовый файл с ингредиентами из корзины пользователя
    и списком рецептов.
    """
    # Получаем текущую дату
    current_date = datetime.today()
    formatted_date = (
        f"{current_date.day} {MONTH_NAMES[current_date.month - 1]} "
        f"{current_date.year}"
    )

    # Создание заголовка с именем пользователя и датой
    header = SHOPPING_LIST_HEADER.format(
        user.username, formatted_date)

    # Создание списка ингредиентов с нумерацией
    ingredients_list = '\n'.join(
        INGREDIENT_FORMAT.format(
            i,
            ingredient['ingredient__name'].capitalize(),
            ingredient['ingredient__measurement_unit'],
            ingredient['amount'])
        for i, ingredient in enumerate(ingredients, start=1)
    )

    # Создание списка рецептов с авторами
    recipes_list = '\n'.join(
        f"{recipe.name} (автор: {recipe.author.username})"
        for recipe in recipes
    )

    # Возврат сформированного списка покупок как строки
    return '\n'.join([
        header,
        'Продукты:',
        ingredients_list,
        'Рецепты:',
        recipes_list,
        '\n\nFoodgram'
    ])
