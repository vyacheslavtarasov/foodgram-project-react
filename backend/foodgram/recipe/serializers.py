import base64

from django.core.files.base import ContentFile
from django.db.models import F
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from recipe.models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    RecipeTag,
    ShoppingCart,
    Tag,
)
from user.serializers import UserSerializer4Djoser


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            ext = format.split("/")[-1]

            data = ContentFile(base64.b64decode(imgstr), name="temp." + ext)

        return super().to_internal_value(data)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_name")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name", "slug", "color")


class RecipeIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeIngredient
        fields = "__all__"


class RecipeTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeTag
        fields = "__all__"


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = "__all__"


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = "__all__"


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

    author = UserSerializer4Djoser(read_only=True)

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

    def validate(self, initial_data):
        if not self.initial_data["tags"]:
            raise serializers.ValidationError(
                "You must assign at least one tag."
            )

        if len(self.initial_data["tags"]) > len(
            set(self.initial_data["tags"])
        ):
            raise serializers.ValidationError("Tags must be unique.")

        if not self.initial_data["ingredients"]:
            raise serializers.ValidationError(
                "You must assign at least one ingredients."
            )

        ingredient_ids = [
            ingredient["id"] for ingredient in self.initial_data["ingredients"]
        ]

        if len(ingredient_ids) > len(set(ingredient_ids)):
            raise serializers.ValidationError("Ingredients must be unique.")

        return initial_data

    def get_ingredients_with_amount(self, obj):
        ret = (
            RecipeIngredient.objects.select_related("recipe")
            .filter(recipe=obj)
            .values(
                "amount",
                "ingredient__id",
                measurement_unit=F("ingredient__measurement_name"),
                name=F("ingredient__name"),
            )
        )
        for entry in list(ret):
            entry["id"] = entry.pop("ingredient__id")
        return ret

    def check_is_favorited(self, obj):
        current_user = self.context["request"].user
        return (
            current_user.is_authenticated
            and Favorite.objects.filter(
                user=self.context["request"].user, recipe=obj
            ).exists()
        )

    def check_is_in_shopping_cart(self, obj):
        current_user = self.context["request"].user
        return (
            current_user.is_authenticated
            and ShoppingCart.objects.filter(
                user=self.context["request"].user, recipe=obj
            ).exists()
        )

    def create(self, validated_data):
        me = Recipe.objects.create(**validated_data)
        tag_list = []
        for tag_id in self.initial_data["tags"]:
            my_tag = get_object_or_404(Tag, id=tag_id)
            tag_list.append(RecipeTag(recipe=me, tag=my_tag))

        RecipeTag.objects.bulk_create(tag_list)
        recipe_list = []
        for ingredient in self.initial_data["ingredients"]:
            ingredient_id = ingredient["id"]
            ingredient_amount = ingredient["amount"]
            my_ingredient = get_object_or_404(Ingredient, id=ingredient_id)

            recipe_list.append(
                RecipeIngredient(
                    recipe=me,
                    ingredient=my_ingredient,
                    amount=ingredient_amount,
                )
            )

        RecipeIngredient.objects.bulk_create(recipe_list)

        return me

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.image = validated_data.get("image", instance.image)
        instance.text = validated_data.get("text", instance.text)
        instance.cooking_time = validated_data.get(
            "cooking_time", instance.cooking_time
        )

        RecipeTag.objects.filter(recipe=instance).delete()
        tag_list = []
        for tag_id in self.initial_data["tags"]:
            my_tag = get_object_or_404(Tag, id=tag_id)

            tag_list.append(RecipeTag(recipe=instance, tag=my_tag))

        RecipeTag.objects.bulk_create(tag_list)

        RecipeIngredient.objects.filter(recipe=instance).delete()
        recipe_list = []
        for ingredient in self.initial_data["ingredients"]:
            ingredient_id = ingredient["id"]
            ingredient_amount = ingredient["amount"]
            my_ingredient = get_object_or_404(Ingredient, id=ingredient_id)

            recipe_list.append(
                RecipeIngredient(
                    recipe=instance,
                    ingredient=my_ingredient,
                    amount=ingredient_amount,
                )
            )

        RecipeIngredient.objects.bulk_create(recipe_list)

        instance.save()
        return instance
