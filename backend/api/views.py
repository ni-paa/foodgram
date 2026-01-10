from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import (GenericViewSet, ModelViewSet,
                                     ReadOnlyModelViewSet,)

from api.filters import IngredientFilter, RecipeFilter
from api.pagination import LimitPagePagination
from api.permissions import IsAuthorAdminAuthenticated
from api.serializers import (FavoriteShoppingCartSerializer,
                             FollowerSerializer, IngredientSerializer,
                             RecipeCreateSerializer, RecipeGetSerializer,
                             TagSerializer, UserSerializer,)
from api.subfile import file_generation
from recipes.models import (FavoriteRecipe, Ingredient, Recipe,
                            RecipeIngredient, ShoppingCart, Tag,)
from users.models import Follower, User


class TagViewSet(ReadOnlyModelViewSet):
    """
    Получение списков тегов и информации о теге по id.
    Создание и редактирование тегов доступно только в админ-панеле.
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny, )
    pagination_class = None


class IngredientViewSet(ReadOnlyModelViewSet):
    """
    Получение списка ингредиентов, информации об ингредиенте по id.
    Создание и редактирование ингредиентов доступно только в админ-панеле.
    Доступен поиск по частичному вхождению в начале названия ингредиента.
    """

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny, )
    filter_backends = (DjangoFilterBackend, )
    filterset_class = IngredientFilter
    pagination_class = None


class RecipeViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.UpdateModelMixin,
                    GenericViewSet):
    """
    Получение списка рецептов, информации о рецепте по id,
    создание/частичное изменение/удаление рецепта по id.
    Изменять рецепт может только автор или админ.
    В списоке рецептов доступна фильтрация по избранному, автору,
    списку покупок и тегам.

    Добавление/удаление рецептов в избранное и список покупок
    для авторизованных пользователей.
    Отправка файла со списком рецептов.
    """

    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorAdminAuthenticated,)
    pagination_class = LimitPagePagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от метода."""

        if self.action == 'list' or self.action == 'retrieve':
            return RecipeGetSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        return serializer.save(author=self.request.user)

    @staticmethod
    def method_post_delete(request, model, add_serializer, pk):
        """
        Вспомогательный метод для методов: def favorite и shopping_cart.
        """

        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            if model.objects.filter(user=user,
                                    recipe=recipe).exists():
                return Response('Вы пытаетесь повторно добавить',
                                status=status.HTTP_400_BAD_REQUEST)
            model.objects.create(user=user, recipe=recipe)
            serializer = add_serializer(recipe)
            return Response(serializer.data, status=status.HTTP_200_OK)
        favorite = model.objects.get(user=user, recipe=recipe)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated],
    )
    def shopping_cart(self, request, pk):
        """Добавление/удаление в список покупок"""

        return self.method_post_delete(request,
                                       ShoppingCart,
                                       FavoriteShoppingCartSerializer,
                                       pk)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, pk):
        return self.method_post_delete(request,
                                       FavoriteRecipe,
                                       FavoriteShoppingCartSerializer,
                                       pk)

    @action(methods=['get'],
            detail=False,
            permission_classes=[IsAuthenticated],)
    def download_shopping_cart(self, request):
        """Создаем список покупок и скачиваем файл со списком покупок."""
        shoppinglist = (RecipeIngredient.objects
                        .filter(recipe__shopping_cart__user=request.user)
                        .values('ingredient__name',
                                'ingredient__measurement_unit')
                        .annotate(amount=Sum('amount')))
        download_list = file_generation(shoppinglist)
        response = HttpResponse(download_list,
                                content_type='text/plain; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="file.txt"'
        return response


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    pagination_class = LimitPagePagination
    lookup_field = 'id'

    @action(methods=('get',),
            detail=False,
            permission_classes=[IsAuthenticated],)
    def me(self, request):
        """Получение пользователем данных о себе (users/me)."""

        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=('post', 'delete',),
            detail=True,
            permission_classes=[IsAuthenticated],)
    def subscribe(self, request, id):
        """Подписаться/отписаться."""

        user = request.user
        author = get_object_or_404(User, id=id)
        if request.method == 'POST':
            if user == author:
                return Response({'message': 'Вы хотите подписаться на себя'},
                                status=status.HTTP_400_BAD_REQUEST)
            Follower.objects.create(user=user, author=author,)
            serializer = FollowerSerializer(author,
                                            context={'request': request},)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            author_del = Follower.objects.filter(user=user, author=author)
            if author_del.exists():
                author_del.delete()
                return Response({'message': 'Вы отписались от автора'},
                                status=status.HTTP_204_NO_CONTENT)

    @action(methods=('get',),
            detail=False,
            permission_classes=[IsAuthenticated],
            serializer_class=FollowerSerializer,)
    def subscriptions(self, request, *args, **kwargs):
        """Получение списка всех подписок на пользователей."""

        user = request.user
        following = User.objects.filter(following__user=user)
        pages = self.paginate_queryset(following)
        if pages is not None:
            serializer = FollowerSerializer(
                pages, many=True, context={'request': request}
            )
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(pages, many=True)
        return Response(serializer.data)
