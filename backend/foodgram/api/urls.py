from django.urls import include, path
from rest_framework import routers

from .views import IngredientsViewSet, RecipesViewSet, TagsViewSet, UserViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register('tags', TagsViewSet, basename='tags')
router.register('ingredients', IngredientsViewSet, basename='ingredients')
router.register('recipes', RecipesViewSet, basename='recipes')
router.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
