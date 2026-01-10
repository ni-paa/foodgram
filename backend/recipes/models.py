from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

from recipes.constants import (MAX_LENGTH_CHARFIELD, MAX_LENGTH_TAG_COLOR,
                               MIN_VALIDATOR_COOK_TIME_INGRED_AMOUNT,
                               REDEX_TAG_SLUG,)
from users.models import User


class Tag(models.Model):
    """
    Класс Тег, для группировки рецептов по тегам.
    Связь полей Recipe через Many-To-Many.
    """

    name = models.CharField(
        max_length=MAX_LENGTH_CHARFIELD,
        verbose_name='Название',
        help_text='Обязательное поле',
        unique=True,
        blank=False,
        null=False,
    )
    color = models.CharField(
        max_length=MAX_LENGTH_TAG_COLOR,
        verbose_name='Цвет',
        help_text='Обязательное поле, Цветовой HEX-код, пример #63C144',
        unique=True,
        blank=False,
        null=False,
    )
    slug = models.SlugField(
        max_length=MAX_LENGTH_CHARFIELD,
        verbose_name='Слаг',
        help_text='Обязательное поле, Латинскими буквами',
        unique=True,
        blank=False,
        null=False,
        validators=[RegexValidator(
            regex=REDEX_TAG_SLUG,
            message='Неверный формат Никнейма')])

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """
    Класс, описывающий ингредиенты.
    Связь с Recipe через модель RecipeIngredient (Many-To-Many).
    """

    name = models.CharField(
        max_length=MAX_LENGTH_CHARFIELD,
        verbose_name='Название',
        help_text='Обязательное поле',
        blank=False,
        null=False,
    )

    measurement_unit = models.CharField(
        max_length=MAX_LENGTH_CHARFIELD,
        verbose_name='Единицы измерения',
        help_text='Обязательное поле',
        blank=False,
        null=False,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    """Класс, описывающий рецепты."""

    name = models.CharField(
        max_length=MAX_LENGTH_CHARFIELD,
        verbose_name='Название',
        help_text='Обязательное поле',
        blank=False,
        null=False,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
        help_text='Обязательное поле',
    )
    text = models.TextField(
        verbose_name='Описание',
        help_text='Обязательное поле',
        blank=False,
        null=False,
    )
    image = models.ImageField(
        verbose_name='Картинка',
        help_text='Обязательное поле',
        upload_to='recipes/',
        blank=False,
        null=False,
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        help_text='Обязательное поле',
        blank=False,
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Список ингредиентов',
        help_text='Обязательное поле',
        blank=False,
        default='морковь',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления (в минутах)',
        help_text='Обязательное поле',
        default=0,
        blank=False,
        null=False,
        validators=[
            MinValueValidator(
                MIN_VALIDATOR_COOK_TIME_INGRED_AMOUNT,
                message=f'Время приготовления должно быть больше или равно'
                        f' {MIN_VALIDATOR_COOK_TIME_INGRED_AMOUNT}'
                        f' минуте')
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return f"Рецепт: {self.name}. Автор: {self.author.username}"


class RecipeIngredient(models.Model):
    """
    Класс для связи модели Recipe и модели Ingredient (Many-To-Many).
    """

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipeingredients',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipeingredients',
        verbose_name='Ингредиент'
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
        blank=False,
        null=False,
        validators=[
            MinValueValidator(
                MIN_VALIDATOR_COOK_TIME_INGRED_AMOUNT,
                message=f'Количество ингредиентов должно быть больше или равно'
                        f' {MIN_VALIDATOR_COOK_TIME_INGRED_AMOUNT}')
        ]
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Количество ингредиентов в рецепте'


class FavoriteRecipe(models.Model):
    """
    Класс, описывающий избранные пользователем рецепты.
    Модель связывает Recipe и User.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='user_recipe_unique_in_favoriterecipe'
            ),
        )

    def __str__(self):
        return f'{self.user.username} добавил {self.recipe.name} в избраннное'


class ShoppingCart(models.Model):
    """
    Класс, описывающий список покупок, который получился
    у пользователя после добавления рецепта(ов) в корзину.
    Модель связывает User и Recipe.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='user_recipe_unique_in_shoppingcart'
            ),
        )

    def __str__(self):
        return (f'{self.user.username} добавил'
                f'{self.recipe.name} в список покупок')
