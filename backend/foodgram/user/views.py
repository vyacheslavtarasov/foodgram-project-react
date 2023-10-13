from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from djoser.views import UserViewSet

from api import paginations
from recipe.models import (
    CustomUser,
)
from user.models import Subscribe
from user.serializers import SubscribeSerializer, UserSerializer

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
        if subscribe_serializer.is_valid(raise_exception=True):
            subscribe_serializer.save()
            user_serializer = UserSerializer(
                my_user_subscribe_on, context={"request": request}, many=False
            )
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        return Response(
            subscribe_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    @subscribe.mapping.delete
    def delete_item_from_subscribe(self, request, id=None):
        my_user_subscribe_on = get_object_or_404(CustomUser, id=id)
        if not get_object_or_404(
            Subscribe,
            user_subscribed_on=my_user_subscribe_on,
            user=request.user,
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
    def subscriptions(self, request, id=None):
        recipes_limit = request.query_params.get("recipes_limit")
        if recipes_limit:
            recipes_limit = int(recipes_limit)

        users = CustomUser.objects.filter(
            id__in=list(
                Subscribe.objects.filter(user=request.user).values_list(
                    "user_subscribed_on", flat=True
                )
            )
        )

        user_serializer = UserSerializer(
            users,
            context={"request": request, "recipes_limit": recipes_limit},
            many=True,
        )

        return self.get_paginated_response(
            self.paginate_queryset(user_serializer.data)
        )
