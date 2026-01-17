from django.urls import path

from .views import index_view, recipe_redirect

urlpatterns = [
    path('', index_view, name='index'),
    path('recipes/<int:pk>/', recipe_redirect, name='recipe-detail'),
    path('s/<int:pk>/', recipe_redirect, name='recipe-redirect'),
]
