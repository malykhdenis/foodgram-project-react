from django_filters import rest_framework as filters

from recipes.models import Recipes, Tags


class RecipesFilter(filters.FilterSet):
    """Recipes' filter."""
    author = filters.NumberFilter(
        field_name='author__id',
        lookup_expr='exact'
    )
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tags.objects.all()
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
        model = Recipes
        fields = ['author', 'tags', 'is_favorited', 'is_in_shopping_cart']

    def filter(self, queryset, name, value):
        if name == 'is_in_shopping_cart' and value:
            queryset = queryset.filter(
                cart__user=self.request.user
            )
        if name == 'is_favorited' and value:
            queryset = queryset.filter(
                favorites__user=self.request.user
            )
        return queryset
