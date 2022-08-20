from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter

from recipes.models import Recipe, Tag


class RecipeFilter(filters.FilterSet):
    """Recipe' filter."""
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    is_favorited = filters.BooleanFilter(
        field_name='is_favorited',
        method='filter',
    )
    is_in_shopping_cart = filters.BooleanFilter(
        field_name='is_in_shopping_cart',
        method='filter',
    )

    class Meta:
        model = Recipe
        fields = ['author', 'tags', 'is_favorited', 'is_in_shopping_cart']

    def filter(self, queryset, name, value):
        if name == 'is_in_shopping_cart' and value:
            return queryset.filter(
                cart__user=self.request.user
            )
        if name == 'is_favorited' and value:
            return queryset.filter(
                favorites__user=self.request.user
            )


class IngredientSearchFilter(SearchFilter):
    """Ingredients' filter."""
    search_param = 'name'
