from rest_framework import serializers
from recipes.models import Ingredients, Recipes, Tags


class TagsSerializer(serializers.ModelSerializer):
    """Tags' serializer."""
    class Meta:
        fields = ('id', 'name', 'color', 'slug',)
        model = Tags


class IngredientsSerializer(serializers.ModelSerializer):
    """Ingredients' serializer."""
    class Meta:
        fields = ('id', 'name', 'measurement_unit',)
        model = Ingredients


class RecipesSerializer(serializers.ModelSerializer):
    """Recipes' serializer."""
    tags = TagsSerializer()
    ingredients = IngredientsSerializer()

    class Meta:
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorite',
                  'is_in_shoping_cart', 'name', 'image', 'text',
                  'cooking_time')
        model = Recipes
