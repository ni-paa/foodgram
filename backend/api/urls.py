from django.urls import include, path
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import routers

from api.views import IngredientViewSet, RecipeViewSet, TagViewSet, UserViewSet

app_name = 'api'

router_v1 = routers.DefaultRouter()

router_v1.register('tags', TagViewSet, basename='tags')
router_v1.register('ingredients',
                   IngredientViewSet,
                   basename='ingredients')
router_v1.register('recipes', RecipeViewSet, basename='recipes')
router_v1.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('users/set_password/',
         DjoserUserViewSet.as_view({'post': 'set_password'})),
    path('auth/', include('djoser.urls.authtoken')),
]

urlpatterns += router_v1.urls
