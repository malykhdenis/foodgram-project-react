from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from drf_extra_fields.fields import Base64ImageField
from backend.foodgram.api.views import RecipesViewSet

from recipes.models import Follows, Ingredients, IngredientsInRecipe, Recipes, Tags
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


class IngredientsInRecipeSerializer(serializers.ModelSerializer):
    """Ingredients in recipe serializer."""
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredientsInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')
        validators = [UniqueTogetherValidator(
            queryset=IngredientsInRecipe.objects.all(),
            fields=['ingredient', 'recipe']
            )
                      ]


class RecipesSerializer(serializers.ModelSerializer):
    """Recipes' serializer."""
    tags = TagsSerializer(read_only=True, many=True)
    ingredients = IngredientsInRecipeSerializer(
        source='ingredientsinrecipe_set', many=True, read_only=True)
    author = UserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shoping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shoping_cart', 'name', 'image', 'text',
                  'cooking_time')
        model = Recipes

    def get_is_favorited(self, obj):
        """Checking if recipe is favorited."""
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipes.objects.filter(favorites__user=user, id=obj.id).exists()

    def get_is_in_shoping_cart(self, obj):
        """Checking if recipe is in shoping cart. """
        user = self.context.get('request').user
        if user.is_anonymous or not user.carts.exists():
            return False
        return Recipes.objects.filter(carts__user=user, id=obj.id).exists()

    def create(self, validated_data):
        """Creating new recipe and relations ingredients in recipe."""
        recipe = Recipes.objects.create(**validated_data)
        ingredients = self.initial_data.get('ingredients')
        tags = self.initial_data.get('tags')
        recipe.tags.set(tags)
        for ingredient in ingredients:
            IngredientsInRecipe.objects.create(
                recipe=recipe, ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount'),)
        return recipe

    def update(self, instance, validated_data):
        """Updating recipe and relations ingredients in recipe."""
        instance.tags.clear()
        tags = self.initial_data.get('tags')
        instance.tags.set(tags)
        IngredientsInRecipe.objects.filter(recipe=instance).all().delete()
        ingredients = self.initial_data.get('ingredients')
        for ingredient in ingredients:
            IngredientsInRecipe.objects.create(
                recipe=instance, ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount'),)
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time)
        instance.save()
        return instance


class CartsSerializer(serializers.ModelSerializer):
    """Carts' serializer."""
    image = Base64ImageField()

    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time',)
        model = Recipes


class FollowsSerializer(serializers.ModelSerializer):
    """Follows' serializer."""
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follows
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        return Follows.objects.filter(user=obj.user,
                                      author=obj.author).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = Recipes.objects.filter(author=obj.author)
        if limit:
            queryset = queryset[:int(limit)]
        return CartsSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return Recipes.objects.filter(author=obj.author).count()
