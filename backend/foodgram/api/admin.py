from django.contrib import admin

from recipe.models import (CustomUser, Favorite, Ingredient, Recipe,
                           RecipeIngredient, RecipeTag, ShoppingCart, Tag)
from user.models import Subscribe


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """Reisters model CustomUser"""

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
    )
    search_fields = ["email", "username"]


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Reisters model Tag"""

    list_display = ("name", "measurement_unit")
    search_fields = ["name"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Reisters model Tag"""

    list_display = (
        "name",
        "slug",
        "color",
    )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Reisters model Recipe"""

    list_display = (
        "id",
        "name",
        "author",
        "text",
        "cooking_time",
        "tag",
        "favorited",
    )
    search_fields = ["name", "author__username", "tags__name"]

    def favorited(self, obj):
        return Favorite.objects.filter(recipe=obj).count()

    def tag(self, obj):
        ret = []
        for val in RecipeTag.objects.filter(recipe=obj):
            ret.append(val.tag)
        return ret


@admin.register(RecipeTag)
class RecipeTagAdmin(admin.ModelAdmin):
    """Reisters model RecipeTag"""

    list_display = (
        "recipe",
        "tag",
    )


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    """Reisters model RecipeIngredient"""

    list_display = ("recipe", "ingredient", "amount")


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Favorite model"""

    list_display = ("recipe", "user")


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """ShoppingCart model"""

    list_display = ("recipe", "user")


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    """Subscribe model"""

    list_display = ("user", "user_subscribed_on")
