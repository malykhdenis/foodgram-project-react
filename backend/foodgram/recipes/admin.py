from django.contrib import admin

from .models import (Carts, Favorites, Follows, Ingredients,
                     IngredientsInRecipe, Recipes, Tags)


class TagsAdmin(admin.ModelAdmin):
    """Admin interface for tags."""
    list_display = ('id', 'name', 'color', 'slug')
    search_fields = ('slug',)
    list_filter = ('color',)


class IngredientsAdmin(admin.ModelAdmin):
    """Admin interface for ingredients."""
    list_display = ('id', 'name', 'measurement_unit',)
    search_fields = ('name',)
    list_filter = ('name', 'measurement_unit',)


class RecipesAdmin(admin.ModelAdmin):
    """Admin interface for recipes."""
    list_display = ('id', 'name', 'author',)
    search_fields = ('name', 'author',)
    list_filter = ('author', 'name', 'tags',)


class IngredientsInRecipeAdmin(admin.ModelAdmin):
    """Admin interface for ingredients in recipes."""
    list_display = ('ingredient', 'recipe', 'amount',)
    search_fields = ('name', 'author',)


class FollowsAdmin(admin.ModelAdmin):
    """Admin interface for follows."""
    list_display = ('user', 'author', 'following_date',)
    search_fields = ('user', 'author',)
    list_filter = ('user', 'author',)


class FavoritesAdmin(admin.ModelAdmin):
    """Admin interface for favorites."""
    list_display = ('user', 'recipe',)
    search_fields = ('user', 'recipe',)
    list_filter = ('user', 'recipe',)


class CartsAdmin(admin.ModelAdmin):
    """Admin interface for carts."""
    list_display = ('user', 'date',)
    search_fields = ('user', 'recipes',)
    list_filter = ('user', 'recipes',)


admin.site.register(Tags, TagsAdmin)
admin.site.register(Ingredients, IngredientsAdmin)
admin.site.register(Recipes, RecipesAdmin)
admin.site.register(IngredientsInRecipe, IngredientsInRecipeAdmin)
admin.site.register(Follows, FollowsAdmin)
admin.site.register(Favorites, FavoritesAdmin)
admin.site.register(Carts, CartsAdmin)
