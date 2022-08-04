from django.contrib import admin

from .models import (Carts, Favorites, Follows, Ingredients,
                     IngredientsInRecipe, Recipes, Tags)

admin.site.register(Tags)
admin.site.register(Ingredients)
admin.site.register(Recipes)
admin.site.register(IngredientsInRecipe)
admin.site.register(Follows)
admin.site.register(Favorites)
admin.site.register(Carts)