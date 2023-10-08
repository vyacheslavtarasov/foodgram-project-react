from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.models import (CustomUser, Favorite, Ingredient, Recipe,
                        RecipeIngredient, ShoppingCart, Subscribe, Tag)
from api.serializers import (IngredientSerializer, RecipeSerializer,
                             TagSerializer)

from .filters import RecipeFilter
from .permissions import RecipePermissions


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
    permission_classes = [RecipePermissions]
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


@api_view(["DELETE", "POST"])
def api_shopping_cart(request, id):
    my_recipe = get_object_or_404(Recipe, id=id)
    if request.method == "POST":
        ShoppingCart.objects.get_or_create(
            recipe=my_recipe, user=request.user
        )
        return Response(
            {
                "id": my_recipe.id,
                "name": my_recipe.name,
                "cooking_time": my_recipe.cooking_time,
                "image": my_recipe.image.url,
            }
        )

    elif request.method == "DELETE":
        ShoppingCart.objects.filter(
            recipe=my_recipe, user=request.user
        ).delete()
        return Response(status=204)


@api_view(["DELETE", "POST"])
def api_favorite(request, id):
    my_recipe = get_object_or_404(Recipe, id=id)
    if request.method == "POST":
        Favorite.objects.get_or_create(recipe=my_recipe, user=request.user)
        return Response(
            {
                "id": my_recipe.id,
                "name": my_recipe.name,
                "cooking_time": my_recipe.cooking_time,
                "image": my_recipe.image.url,
            }
        )

    elif request.method == "DELETE":
        Favorite.objects.filter(recipe=my_recipe, user=request.user).delete()
        return Response(status=204)


@api_view(["GET"])
def api_subscriptions(request):
    recipes_limit = request.query_params.get("recipes_limit")

    my_subscriptions = Subscribe.objects.filter(user=request.user)

    entries = []
    for entry in my_subscriptions:
        my_recipes = Recipe.objects.filter(author=entry.user_subscribed_on)
        if recipes_limit is not None and my_recipes.count() > int(
            recipes_limit
        ):
            continue
        data2return = {}
        data2return["id"] = entry.user_subscribed_on.id
        data2return["email"] = entry.user_subscribed_on.email
        data2return["first_name"] = entry.user_subscribed_on.first_name
        data2return["last_name"] = entry.user_subscribed_on.last_name
        data2return["is_subscribed"] = True

        data2return["recipes"] = []
        for my_recipe in my_recipes:
            data2return["recipes"].append(
                {
                    "id": my_recipe.id,
                    "name": my_recipe.name,
                    "cooking_time": my_recipe.cooking_time,
                    "image": my_recipe.image.url,
                }
            )
        data2return["recipes_count"] = my_recipes.count()

        entries.append(data2return)
    paginator = PageNumberPagination()
    paginator.page_size = 20
    result_page = paginator.paginate_queryset(entries, request)
    return paginator.get_paginated_response(result_page)


@api_view(["GET"])
def api_download_shopping_cart(request):
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


@api_view(["POST", "DELETE"])
def api_subscribe(request, id):
    my_user_subscribe_on = get_object_or_404(CustomUser, id=id)
    recipes_limit = request.query_params.get("recipes_limit")
    if request.method == "POST":
        my_recipes = Recipe.objects.filter(author=my_user_subscribe_on)
        if recipes_limit is not None and my_recipes.count() > int(
            recipes_limit
        ):
            return Response(
                {"error": "amount of recepies is too big"}, status=400
            )
        Subscribe.objects.get_or_create(
            user_subscribed_on=my_user_subscribe_on, user=request.user
        )
        data2return = {}
        data2return["id"] = my_user_subscribe_on.id
        data2return["email"] = my_user_subscribe_on.email
        data2return["first_name"] = my_user_subscribe_on.first_name
        data2return["last_name"] = my_user_subscribe_on.last_name
        data2return["is_subscribed"] = True

        data2return["recipes"] = []
        for my_recipe in my_recipes:
            data2return["recipes"].append(
                {
                    "id": my_recipe.id,
                    "name": my_recipe.name,
                    "cooking_time": my_recipe.cooking_time,
                    "image": my_recipe.image.url,
                }
            )
        data2return["recipes_count"] = my_recipes.count()
        return Response(data2return, status=204)

    elif request.method == "DELETE":
        Subscribe.objects.filter(
            user_subscribed_on=my_user_subscribe_on, user=request.user
        ).delete()
        return Response(status=204)
