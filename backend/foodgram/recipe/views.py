from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from djoser.views import UserViewSet

from api.models import (CustomUser, Favorite, Ingredient, Recipe,
                        RecipeIngredient, ShoppingCart, Subscribe, Tag)
from api.serializers import (IngredientSerializer,
                             TagSerializer, ShoppingCartSerializer, FavoriteSerializer, SubscribeSerializer)
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
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated],)
    def shopping_cart(self, request, id=None):
        my_recipe = get_object_or_404(Recipe, id=id)
        shopping_cart_serializer = ShoppingCartSerializer(data={"user": self.request.user.id, "recipe": my_recipe.id})
        if shopping_cart_serializer.is_valid():
            shopping_cart_serializer.save()
            return Response(
                {
                    "id": my_recipe.id,
                    "name": my_recipe.name,
                    "cooking_time": my_recipe.cooking_time,
                    "image": my_recipe.image.url,
                }, status=status.HTTP_200_OK)
        return Response(shopping_cart_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @shopping_cart.mapping.delete
    def delete_item_from_shopping_cart(self, request, id=None):
        my_recipe = get_object_or_404(Recipe, id=id)
        if (ShoppingCart.objects.filter(
                recipe=my_recipe, user=request.user
            ).delete()[0] != 0):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"errors": "Delete operation failed."}, status=status.HTTP_400_BAD_REQUEST)



    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated],)
    def favorite(self, request, id=None):
        my_recipe = get_object_or_404(Recipe, id=id)
        favorite_serializer = FavoriteSerializer(data={"user": self.request.user.id, "recipe": my_recipe.id})
        if favorite_serializer.is_valid():
            favorite_serializer.save()
            return Response(
                {
                    "id": my_recipe.id,
                    "name": my_recipe.name,
                    "cooking_time": my_recipe.cooking_time,
                    "image": my_recipe.image.url,
                }, 
                status=status.HTTP_200_OK)
        return Response(favorite_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @favorite.mapping.delete
    def delete_item_from_favorite(self, request, id=None):
        my_recipe = get_object_or_404(Recipe, id=id)
        if (Favorite.objects.filter(
                recipe=my_recipe, user=request.user
            ).delete()[0] != 0):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"errors": "Delete operation failed."}, status=status.HTTP_400_BAD_REQUEST)


    

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated],)
    def download_shopping_cart(self, request, id=None):
        cart = ShoppingCart.objects.filter(user=request.user)

        ret = {}
        for entry in cart:
            recipe = entry.recipe
            recipe_ingredients = RecipeIngredient.objects.filter(recipe=recipe)
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
