from rest_framework import serializers

from recipes.models import Ingredients, Recipes, Tags
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


class RecipesSerializer(serializers.ModelSerializer):
    """Recipes' serializer."""
    tags = TagsSerializer()
    ingredients = IngredientsSerializer()
    author = UserSerializer()
    is_favorited = serializers.SerializerMethodField()
    is_in_shoping_cart = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shoping_cart', 'name', 'image', 'text',
                  'cooking_time')
        model = Recipes

    def get_is_favorited(self, obj):
        """Checking if recipe is favorited."""
        user = self.context.get('request').user
        if user.is_anonymous or user == obj.author:
            return False
        return user.favorites.filter(id=obj.id).exists()

    def get_is_in_shoping_cart(self, obj):
        """Checking if recipe is in shoping cart. """
        user = self.context.get('request').user
        if user.is_anonymous or not user.carts.exists():
            return False
        return user.carts.recipes.filter(id=obj.id).exists()
