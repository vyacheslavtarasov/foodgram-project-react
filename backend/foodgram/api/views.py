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
from api.serializers import (IngredientSerializer, RecipeSerializer,
                             TagSerializer, ShoppingCartSerializer, FavoriteSerializer, SubscribeSerializer)

from .filters import RecipeFilter
from .permissions import Browse4AllEdit4Author, IsAuthenticated


class TagViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    Get all Tags.
    """

    pagination_class = None
    permission_classes = [AllowAny]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = "id"


class IngredientViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    Get all Ingredients.
    """

    pagination_class = None
    permission_classes = [AllowAny]
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)

    search_fields = ["name"]

    lookup_field = "id"
    search_fields = ("name",)


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


class CustomUserViewSet(UserViewSet):

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated],)
    def subscribe(self, request, id=None):
        my_user_subscribe_on = get_object_or_404(CustomUser, id=id)
        subscribe_serializer = SubscribeSerializer(data={"user_subscribed_on": my_user_subscribe_on.id, "user": request.user.id})
        my_recipes = Recipe.objects.filter(author=my_user_subscribe_on)
        if subscribe_serializer.is_valid():
            subscribe_serializer.save()
            return Response(
                {
                    "id": my_user_subscribe_on.id,
                    "email": my_user_subscribe_on.email,
                    "first_name": my_user_subscribe_on.first_name,
                    "last_name": my_user_subscribe_on.last_name,
                    "is_subscribed": True,
                    "recipes_count": my_recipes.count(),
                    "recipes": my_recipes.values("id", "name", "cooking_time", "image")
                }, status=status.HTTP_200_OK)
        return Response(subscribe_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @subscribe.mapping.delete
    def delete_item_from_subscribe(self, request, id=None):
        my_user_subscribe_on = get_object_or_404(CustomUser, id=id)
        if (Subscribe.objects.filter(
                user_subscribed_on=my_user_subscribe_on, user=request.user
            ).delete()[0] != 0):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"errors": "Delete operation failed."}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated],)
    def subscriptions(self, request, id=None):
        recipes_limit = request.query_params.get("recipes_limit")
        if recipes_limit:
            recipes_limit = int(recipes_limit)
        my_subscriptions = Subscribe.objects.filter(user=request.user)

        entries = []
        for entry in my_subscriptions:
            my_recipes = Recipe.objects.filter(author=entry.user_subscribed_on)
            entries.append({
                "id": entry.user_subscribed_on.id,
                "email": entry.user_subscribed_on.email,
                "first_name": entry.user_subscribed_on.first_name,
                "last_name": entry.user_subscribed_on.last_name,
                "is_subscribed": True,
                "recipes_count": my_recipes.count(),
                "recipes": my_recipes.values("id", "name", "cooking_time", "image").order_by("-id")[:recipes_limit],
            })
        paginator = PageNumberPagination()
        paginator.page_size = 20
        result_page = paginator.paginate_queryset(entries, request)
        return paginator.get_paginated_response(result_page)





# @api_view(["GET"])
# def api_subscriptions(request):
#     recipes_limit = request.query_params.get("recipes_limit")

#     my_subscriptions = Subscribe.objects.filter(user=request.user)

#     entries = []
#     for entry in my_subscriptions:
#         my_recipes = Recipe.objects.filter(author=entry.user_subscribed_on)
#         if recipes_limit is not None and my_recipes.count() > int(
#             recipes_limit
#         ):
#             continue
#         data2return = {}
#         data2return["id"] = entry.user_subscribed_on.id
#         data2return["email"] = entry.user_subscribed_on.email
#         data2return["first_name"] = entry.user_subscribed_on.first_name
#         data2return["last_name"] = entry.user_subscribed_on.last_name
#         data2return["is_subscribed"] = True

#         data2return["recipes"] = []
#         for my_recipe in my_recipes:
#             data2return["recipes"].append(
#                 {
#                     "id": my_recipe.id,
#                     "name": my_recipe.name,
#                     "cooking_time": my_recipe.cooking_time,
#                     "image": my_recipe.image.url,
#                 }
#             )
#         data2return["recipes_count"] = my_recipes.count()

#         entries.append(data2return)


#     paginator = PageNumberPagination()
#     paginator.page_size = 20
#     result_page = paginator.paginate_queryset(entries, request)
#     return paginator.get_paginated_response(result_page)


