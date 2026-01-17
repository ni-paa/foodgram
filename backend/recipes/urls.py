from django.urls import path

from .views import IndexView, recipe_redirect

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('recipes/<int:pk>/', recipe_redirect, name='recipe-detail'),
    path('s/<int:pk>/', recipe_redirect, name='recipe-redirect'),
]
