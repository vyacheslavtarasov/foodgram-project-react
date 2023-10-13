from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


from recipe.models import (
    Favorite,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
)
from recipe.serializers import (
    ShoppingCartSerializer,
    FavoriteSerializer,
)
from recipe.serializers import RecipeSerializer

from api.filters import RecipeFilter
from api.permissions import Browse4AllEdit4Author, IsAuthenticated


class RecipeViewSet(
    viewsets.ModelViewSet,
):

    """
    Получить список всех категорий.
    """

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [Browse4AllEdit4Author]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    lookup_field = "id"
    search_fields = ("name",)

    def perform_create(self, serializer):
        serializer.save(
            is_favorited=False,
            is_in_shopping_cart=False,
            author=self.request.user,
        )

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsAuthenticated],
    )
    def shopping_cart(self, request, id=None):
        my_recipe = get_object_or_404(Recipe, id=id)
        recipe_serializer = RecipeSerializer(
            my_recipe, context={"request": request}
        )

        shopping_cart_serializer = ShoppingCartSerializer(
            data={"user": self.request.user.id, "recipe": my_recipe.id}
        )
        if shopping_cart_serializer.is_valid(raise_exception=True):
            shopping_cart_serializer.save()
            necessary_fields = ["id", "name", "cooking_time", "image"]
            return Response(
                {key: recipe_serializer.data[key] for key in necessary_fields},
                status=status.HTTP_200_OK,
            )
        return Response(
            shopping_cart_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    @shopping_cart.mapping.delete
    def delete_item_from_shopping_cart(self, request, id=None):
        my_recipe = get_object_or_404(Recipe, id=id)
        if not get_object_or_404(
            ShoppingCart, recipe=my_recipe, user=request.user
        ).delete():
            return Response(
                {"errors": "Delete operation failed."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, id=None):
        my_recipe = get_object_or_404(Recipe, id=id)
        recipe_serializer = RecipeSerializer(
            my_recipe, context={"request": request}
        )

        favorite_serializer = FavoriteSerializer(
            data={"user": self.request.user.id, "recipe": my_recipe.id}
        )
        if favorite_serializer.is_valid(raise_exception=True):
            favorite_serializer.save()
            necessary_fields = ["id", "name", "cooking_time", "image"]
            return Response(
                {key: recipe_serializer.data[key] for key in necessary_fields},
                status=status.HTTP_200_OK,
            )
        return Response(
            favorite_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    @favorite.mapping.delete
    def delete_item_from_favorite(self, request, id=None):
        my_recipe = get_object_or_404(Recipe, id=id)
        if not get_object_or_404(
            Favorite, recipe=my_recipe, user=self.request.user
        ).delete():
            return Response(
                {"errors": "Delete operation failed."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated],
    )
    def download_shopping_cart(self, request, id=None):
        cart = ShoppingCart.objects.filter(user=self.request.user)

        ret = {}
        for entry in cart:
            recipe = entry.recipe
            recipe_ingredients = RecipeIngredient.objects.filter(
                recipe=recipe
            ).order_by("name")
            for recipe_ingredient in recipe_ingredients:
                if recipe_ingredient.ingredient.name in ret:
                    ret[
                        recipe_ingredient.ingredient.name
                    ] += recipe_ingredient.amount
                else:
                    ret[
                        recipe_ingredient.ingredient.name
                    ] = recipe_ingredient.amount
        pr = ""
        for key, value in ret.items():
            pr += f"{key}\t{value}\n"

        response = HttpResponse(pr, content_type="text/plain")
        response["Content-Disposition"] = 'attachment; filename="1.txt"'
        return response
