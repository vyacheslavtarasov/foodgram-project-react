from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from djoser.views import UserViewSet

from api.models import (
    CustomUser,
    Recipe,
    Subscribe,
)
from api.serializers import (
    SubscribeSerializer,
)

from api.permissions import IsAuthenticated


class CustomUserViewSet(UserViewSet):
    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request, id=None):
        my_user_subscribe_on = get_object_or_404(CustomUser, id=id)
        subscribe_serializer = SubscribeSerializer(
            data={
                "user_subscribed_on": my_user_subscribe_on.id,
                "user": request.user.id,
            }
        )
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
                    "recipes": my_recipes.values(
                        "id", "name", "cooking_time", "image"
                    ),
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            subscribe_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    @subscribe.mapping.delete
    def delete_item_from_subscribe(self, request, id=None):
        my_user_subscribe_on = get_object_or_404(CustomUser, id=id)
        if (
            Subscribe.objects.filter(
                user_subscribed_on=my_user_subscribe_on, user=request.user
            ).delete()[0]
            != 0
        ):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {"errors": "Delete operation failed."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated],
    )
    def subscriptions(self, request, id=None):
        recipes_limit = request.query_params.get("recipes_limit")
        if recipes_limit:
            recipes_limit = int(recipes_limit)
        my_subscriptions = Subscribe.objects.filter(
            user=request.user
        ).select_related("user_subscribed_on")

        # firstnames = CustomUser.objects.filter(user=request.user)
        # .values_list('user_subscribed_on') 
        # print(list(firstnames))
        entries = []
        for entry in my_subscriptions:
            my_recipes = Recipe.objects.filter(author=entry.user_subscribed_on)
            data_2_return = []
            for my_recipe in my_recipes:
                data_2_return.append(
                    {
                        "id": my_recipe.id,
                        "name": my_recipe.name,
                        "cooking_time": my_recipe.cooking_time,
                        "image": my_recipe.image.url,
                    }
                )

            entries.append(
                {
                    "id": entry.user_subscribed_on.id,
                    "email": entry.user_subscribed_on.email,
                    "first_name": entry.user_subscribed_on.first_name,
                    "last_name": entry.user_subscribed_on.last_name,
                    "is_subscribed": True,
                    "recipes_count": my_recipes.count(),
                    "recipes": data_2_return,
                    # my_recipes.values("id", "name", "cooking_time", "image").
                    # order_by("-id")[:recipes_limit]
                }
            )
        paginator = PageNumberPagination()
        paginator.page_size = 20
        result_page = paginator.paginate_queryset(entries, request)
        return paginator.get_paginated_response(result_page)
