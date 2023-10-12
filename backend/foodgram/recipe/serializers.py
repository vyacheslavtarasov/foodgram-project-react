import base64

from django.core.files.base import ContentFile
from django.db.models import F
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api.models import (CustomUser, Favorite, Ingredient, Recipe,
                        RecipeIngredient, RecipeTag, ShoppingCart, Subscribe,
                        Tag)
from user.serializers import UserSerializer
from api.serializers import TagSerializer


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            ext = format.split("/")[-1]

            data = ContentFile(base64.b64decode(imgstr), name="temp." + ext)

        return super().to_internal_value(data)


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False, allow_null=True)

    tags = TagSerializer(many=True, read_only=True)
    ingredients = serializers.SerializerMethodField(
        "get_ingredients_with_amount",
        read_only=True,
    )
    is_favorited = serializers.SerializerMethodField(
        "check_is_favorited", read_only=True
    )

    is_in_shopping_cart = serializers.SerializerMethodField(
        "check_is_in_shopping_cart", read_only=True
    )

    author = UserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "text",
            "cooking_time",
            "tags",
            "author",
            "ingredients",
            "image",
            "is_favorited",
            "is_in_shopping_cart",
        )

    def get_ingredients_with_amount(self, obj):

        ret = RecipeIngredient.objects.select_related('recipe').filter(recipe=obj).values("amount", "ingredient__id", measurement_unit=F('ingredient__measurement_name'), name=F('ingredient__name'))
        for entry in list(ret):
            entry["id"] = entry.pop("ingredient__id")

        return ret

    def check_is_favorited(self, obj):
        current_user = self.context["request"].user
        return current_user.is_authenticated and Favorite.objects.filter(
                user=self.context["request"].user, recipe=obj).exists()

    def check_is_in_shopping_cart(self, obj):
        current_user = self.context["request"].user
        return current_user.is_authenticated and ShoppingCart.objects.filter(
                user=self.context["request"].user, recipe=obj).exists()

    def create(self, validated_data):
        me = Recipe.objects.create(**validated_data)
        t_objects_list = []
        for tag_id in self.initial_data["tags"]:
            my_tag = get_object_or_404(Tag, id=tag_id)

            t_objects_list.append(RecipeTag(recipe=me, tag=my_tag))

        RecipeTag.objects.bulk_create(t_objects_list)

        re_objects_list = []
        for ingredient in self.initial_data["ingredients"]:
            ingredient_id = ingredient["id"]
            ingredient_amount = ingredient["amount"]
            my_ingredient = get_object_or_404(Ingredient, id=ingredient_id)
            
            re_objects_list.append(RecipeIngredient(recipe=me, ingredient=my_ingredient, amount=ingredient_amount))

        RecipeIngredient.objects.bulk_create(re_objects_list)

        return me

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.image = validated_data.get("image", instance.image)
        instance.text = validated_data.get("text", instance.text)
        instance.cooking_time = validated_data.get(
            "cooking_time", instance.cooking_time
        )

        RecipeTag.objects.filter(recipe=instance).delete()
        t_objects_list = []
        for tag_id in self.initial_data["tags"]:
            my_tag = get_object_or_404(Tag, id=tag_id)

            t_objects_list.append(RecipeTag(recipe=instance, tag=my_tag))

        RecipeTag.objects.bulk_create(t_objects_list)

        RecipeIngredient.objects.filter(recipe=instance).delete()
        re_objects_list = []
        for ingredient in self.initial_data["ingredients"]:
            ingredient_id = ingredient["id"]
            ingredient_amount = ingredient["amount"]
            my_ingredient = get_object_or_404(Ingredient, id=ingredient_id)
            
            re_objects_list.append(RecipeIngredient(recipe=instance, ingredient=my_ingredient, amount=ingredient_amount))

        RecipeIngredient.objects.bulk_create(re_objects_list)

        instance.save()
        return instance