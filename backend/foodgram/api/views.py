from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

import logging
logger = logging.getLogger(__name__)
from rest_framework import viewsets
from api.serializers import (
    TagSerializer,
    IngredientSerializer,
    RecipeSerializer,
    FavoriteSerializer,
    UserSerializer
)
from django.shortcuts import get_object_or_404
from api.models import Ingredients, Tag, Recipe, CustomUser, Favorite, Subscribe
from rest_framework import filters, mixins, permissions, status, viewsets

class TagViewSet(
    viewsets.ModelViewSet,
    # mixins.CreateModelMixin,
    # mixins.ListModelMixin,
    # mixins.DestroyModelMixin,
    # mixins.RetrieveModelMixin,
    # viewsets.GenericViewSet,
):
    """
    Получить список всех Тегов.
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    # permission_classes = (IsAdminOrReadOnly,)
    # filter_backends = (SearchFilter,)
    # search_fields = ("name",)
    lookup_field = "id"


class IngredientViewSet(
    # mixins.CreateModelMixin,
    mixins.ListModelMixin,
    # mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    Получить список всех Ингредиентов.
    """

    queryset = Ingredients.objects.all()
    serializer_class = IngredientSerializer
    lookup_field = "id"
    search_fields = ("name",)

class RecipeViewSet(
    viewsets.ModelViewSet,
    # viewsets.GenericViewSet,
    # mixins.CreateModelMixin,
    # mixins.ListModelMixin,
    # mixins.DestroyModelMixin,
    
):
    

    """
    Получить список всех категорий.
    """
    permission_classes = [AllowAny]
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    # pagination_class = PageNumberPagination
    # permission_classes = (IsAdminOrReadOnly,)
    # filter_backends = (SearchFilter,)

    lookup_field = "id"
    search_fields = ("name",)


    def perform_create(self, serializer):
        serializer.save(is_favorited=False, is_in_shopping_cart=False, author=self.request.user)
    
@api_view(['DELETE', 'POST'])
def api_favorite(request, id):
    my_recipe = get_object_or_404(Recipe, id=id)
    if request.method == 'POST':
        Favorite.objects.get_or_create(recipe=my_recipe, user=request.user)
        # all_favorites = Favorite.objects.all()
        # serializer = FavoriteSerializer(all_favorites, many=True)
        return Response({"id": my_recipe.id, "name": my_recipe.name, "cooking_time": my_recipe.cooking_time, "image": my_recipe.image.url})
        
    elif request.method == "DELETE":
        Favorite.objects.filter(recipe=my_recipe, user=request.user).delete()
        return Response({"errors": "",}, status=status.HTTP_201_CREATED)
    

@api_view(['GET'])
def api_subscriptions(request):
    my_subscriptions = Subscribe.objects.filter(user=request.user)
    # paginator = PageNumberPagination()
    # paginator.page_size = 10
    # person_objects = Person.objects.all()
    # result_page = paginator.paginate_queryset(person_objects, request)
    # serializer = PersonSerializer(result_page, many=True)
    # return paginator.get_paginated_response(serializer.data)
    return Response({"errors": "asdf",}, status=status.HTTP_201_CREATED)

@api_view(['POST', 'DELETE'])
def api_subscribe(request, id):
    my_user_subscribe_on = get_object_or_404(CustomUser, id=id)
    if request.method == 'POST':
        Subscribe.objects.get_or_create(user_subscribed_on=my_user_subscribe_on, user=request.user)
        data2return = {}
        data2return["id"] = my_user_subscribe_on.id
        data2return["email"] = my_user_subscribe_on.email
        data2return["first_name"] = my_user_subscribe_on.first_name
        data2return["last_name"] = my_user_subscribe_on.last_name
        data2return["is_subscribed"] = True
        my_recipes = Recipe.objects.filter(author=my_user_subscribe_on)
        data2return["recipes"] = []
        for my_recipe in my_recipes:
            data2return["recipes"].append({"id": my_recipe.id, "name": my_recipe.name, "cooking_time": my_recipe.cooking_time, "image": my_recipe.image.url})
        data2return["recipes_count"] = my_recipes.count()
        return Response(data2return, status=204)
        
    elif request.method == "DELETE":
        Favorite.objects.filter(recipe=my_recipe, user=request.user).delete()
        return Response({"errors": "",}, status=status.HTTP_201_CREATED)
    