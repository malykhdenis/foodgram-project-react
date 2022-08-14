from django.contrib import admin

from .models import (Cart, Favorite, Follow, Ingredient,
                     IngredientInRecipe, Recipe, Tag)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin interface for tags."""
    list_display = ('id', 'name', 'color', 'slug')
    search_fields = ('slug',)
    list_filter = ('color',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Admin interface for ingredients."""
    list_display = ('id', 'name', 'measurement_unit',)
    search_fields = ('name',)
    list_filter = ('name', 'measurement_unit',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Admin interface for recipes."""
    list_display = ('id', 'name', 'author', 'favorites')
    search_fields = ('name', 'author',)
    list_filter = ('author', 'name', 'tags',)

    def favorites(self, obj):
        """Counting recipe in favorites."""
        return obj.favorites.count()


@admin.register(IngredientInRecipe)
class IngredientInRecipeAdmin(admin.ModelAdmin):
    """Admin interface for ingredients in recipes."""
    list_display = ('ingredient', 'recipe', 'amount',)
    search_fields = ('name', 'author',)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Admin interface for follows."""
    list_display = ('user', 'author', 'following_date',)
    search_fields = ('user', 'author',)
    list_filter = ('user', 'author',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Admin interface for favorites."""
    list_display = ('user', 'recipe',)
    search_fields = ('user', 'recipe',)
    list_filter = ('user', 'recipe',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Admin interface for carts."""
    list_display = ('user', 'date',)
    search_fields = ('user', 'recipe',)
    list_filter = ('user', 'recipe',)
