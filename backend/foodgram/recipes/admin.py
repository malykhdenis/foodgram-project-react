from django.contrib import admin

from .models import (Carts, Favorites, Follows, Ingredients,
                     IngredientsInRecipe, Recipes, Tags)


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    """Admin interface for tags."""
    list_display = ('id', 'name', 'color', 'slug')
    search_fields = ('slug',)
    list_filter = ('color',)


@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    """Admin interface for ingredients."""
    list_display = ('id', 'name', 'measurement_unit',)
    search_fields = ('name',)
    list_filter = ('name', 'measurement_unit',)


@admin.register(Recipes)
class RecipesAdmin(admin.ModelAdmin):
    """Admin interface for recipes."""
    list_display = ('id', 'name', 'author',)
    search_fields = ('name', 'author',)
    list_filter = ('author', 'name', 'tags',)


@admin.register(IngredientsInRecipe)
class IngredientsInRecipeAdmin(admin.ModelAdmin):
    """Admin interface for ingredients in recipes."""
    list_display = ('ingredient', 'recipe', 'amount',)
    search_fields = ('name', 'author',)


@admin.register(Follows)
class FollowsAdmin(admin.ModelAdmin):
    """Admin interface for follows."""
    list_display = ('user', 'author', 'following_date',)
    search_fields = ('user', 'author',)
    list_filter = ('user', 'author',)


@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    """Admin interface for favorites."""
    list_display = ('user', 'recipe',)
    search_fields = ('user', 'recipe',)
    list_filter = ('user', 'recipe',)


@admin.register(Carts)
class CartsAdmin(admin.ModelAdmin):
    """Admin interface for carts."""
    list_display = ('user', 'date',)
    search_fields = ('user', 'recipes',)
    list_filter = ('user', 'recipes',)
