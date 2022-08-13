from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.serializers import ValidationError

from recipes.models import (Follow, Ingredient, IngredientInRecipe, Recipe,
                            Tag)
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Users' serializer."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed',)
        model = User
        read_only_fields = 'is_subscribed',

    def get_is_subscribed(self, obj):
        '''Checking if user is subscribed.'''
        user = self.context.get('request').user
        if user.is_anonymous or user == obj:
            return False
        return user.follower.filter(id=obj.id).exists()


class UserCreateSerializer(serializers.ModelSerializer):
    """Users' serializer."""
    class Meta:
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'password')
        model = User
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """User registration."""
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class TagSerializer(serializers.ModelSerializer):
    """Tag' serializer."""
    class Meta:
        fields = ('id', 'name', 'color', 'slug',)
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    """Ingredient' serializer."""
    class Meta:
        fields = ('id', 'name', 'measurement_unit',)
        model = Ingredient


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    """Ingredient in recipe serializer."""
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')
        validators = [UniqueTogetherValidator(
            queryset=IngredientInRecipe.objects.all(),
            fields=['ingredient', 'recipe']
            )
                      ]


class RecipeSerializer(serializers.ModelSerializer):
    """Recipe' serializer."""
    tags = TagSerializer(read_only=True, many=True)
    ingredients = IngredientInRecipeSerializer(
        source='ingredientinrecipe_set', many=True, read_only=True)
    author = UserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shoping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shoping_cart', 'name', 'image', 'text',
                  'cooking_time')
        model = Recipe

    def check_double_item(self, data):
        validated_items = []
        for item in data:
            if item in validated_items:
                raise ValidationError('Ошибка оригинальности поля')
            validated_items.append(item)

    def validate(self, data):
        tags = self.initial_data.get('tags')
        ingredients = self.initial_data.get('ingredients')
        ingredients_id = [i['id'] for i in ingredients]
        pass
        self.check_double_item(tags)
        self.check_double_item(ingredients_id)
        data['tags'] = tags
        data['ingredients'] = ingredients
        return data

    def get_is_favorited(self, obj):
        """Checking if recipe is favorited."""
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(favorites__user=user, id=obj.id).exists()

    def get_is_in_shoping_cart(self, obj):
        """Checking if recipe is in shoping cart. """
        user = self.context.get('request').user
        if user.is_anonymous or not user.carts.exists():
            return False
        return Recipe.objects.filter(cart__user=user, id=obj.id).exists()

    def create(self, validated_data):
        """Creating new recipe and relations ingredients in recipe."""
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        new_ingredients = [
            IngredientInRecipe(
                recipe=recipe,
                ingredient=get_object_or_404(
                    Ingredient,
                    id=ingredient['id'],
                ),
                amount=ingredient['amount'],
            )
            for ingredient in ingredients
        ]
        IngredientInRecipe.objects.bulk_create(objs=new_ingredients)
        recipe.tags.set(tags)
        return recipe

    def update(self, instance, validated_data):
        """Updating recipe and relations ingredients in recipe."""
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance.ingredients.clear()
        instance.tags.clear()
        IngredientInRecipe.objects.filter(recipe=instance).delete()
        new_ingredients = [
            IngredientInRecipe(
                recipe=instance,
                ingredient=get_object_or_404(
                    Ingredient,
                    id=ingredient['id'],
                ),
                amount=ingredient['amount'],
            )
            for ingredient in ingredients
        ]
        IngredientInRecipe.objects.bulk_create(objs=new_ingredients)
        instance.tags.set(tags)
        return super().update(instance, validated_data)


class CartSerializer(serializers.ModelSerializer):
    """Cart' serializer."""
    image = Base64ImageField()

    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time',)
        model = Recipe


class FollowSerializer(serializers.ModelSerializer):
    """Follow' serializer."""
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        """"Checking if user is subscribed."""
        return Follow.objects.filter(user=obj.user,
                                     author=obj.author).exists()

    def get_recipes(self, obj):
        """All users' recipes with limit."""
        request = self.context.get('request')
        recipes_limit = request.GET.get('recipes_limit')
        recipes = Recipe.objects.filter(author=obj.author)
        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]
        serializer = CartSerializer(recipes, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        """Recipe' count."""
        return Recipe.objects.filter(author=obj.author).count()


class SetPasswordSerializer(serializers.ModelSerializer):
    """Serializer for setting password checking."""
    new_password = serializers.CharField()
    current_password = serializers.CharField()

    class Meta:
        model = User
        fields = ('new_password', 'current_password')
