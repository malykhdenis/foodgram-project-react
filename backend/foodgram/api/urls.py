from django.urls import include, path
from rest_framework import routers

# from djoser.views import UserViewSet as DjoserViewSet

from .views import (IngredientsViewSet, RecipesViewSet, TagsViewSet,
                    UserMeViewSet, UserViewSet,)

app_name = 'api'

router = routers.DefaultRouter()
router.register('tags', TagsViewSet, basename='tags')
router.register('ingredients', IngredientsViewSet, basename='ingredients')
router.register('recipes', RecipesViewSet, basename='recipes')
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('users/me/', UserMeViewSet.as_view({'get': 'list'})),
    # path('', include(router.urls)),
    # path('users/set_password/', UserPassword.as_view({'post': 'list'})),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
