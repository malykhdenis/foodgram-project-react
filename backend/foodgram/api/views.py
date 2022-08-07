from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from djoser.views import UserViewSet as DjoserViewSet

from recipes.models import Ingredients, Recipes, Tags
from users.models import User

from .serializers import (IngredientsSerializer, TagsSerializer,
                          UserSerializer, UserCreateSerializer)


class UserViewSet(DjoserViewSet):
    """Users' viewset."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserSerializer


class TagsViewSet(viewsets.ModelViewSet):
    """Tags' viewset."""
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer


class IngredientsViewSet(viewsets.ModelViewSet):
    """Ingredients' viewset."""
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    """Ingredients' viewset."""
    queryset = Recipes.objects.all()
    serializer_class = IngredientsSerializer
    paginator_class = LimitOffsetPagination
