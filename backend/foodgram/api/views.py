from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from recipes.models import Ingredients, Recipes, Tags
from .serializers import TagsSerializer, IngredientsSerializer


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
