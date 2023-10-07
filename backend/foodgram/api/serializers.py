from rest_framework import serializers
import base64
from django.shortcuts import get_object_or_404

from api.models import Ingredient, Tag, CustomUser, Recipe, RecipeTag, RecipeIngredient, Favorite, ShoppingCart, Subscribe
from django.core.files.base import ContentFile
from .validators import UsernameValidatorRegex

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    is_subscribed = serializers.SerializerMethodField(
        'check_is_subscribed',
        read_only=True
    )
    class Meta:
        model = CustomUser
        fields = ["username", "id", "password", "email", "last_name", "first_name", "is_subscribed"]

    def check_is_subscribed(self, obj):
        if self.context['request'].user.is_authenticated and Subscribe.objects.filter(user=self.context['request'].user, user_subscribed_on=obj).exists():
            return True
        return False

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_name")

class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)

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

class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = "__all__"

class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False, allow_null=True)

    image_url = serializers.SerializerMethodField(
        'get_image_url',
        read_only=True,
    )

    tags = TagSerializer(many=True, read_only=True)
    ingredients = serializers.SerializerMethodField(
        'get_ingredients_with_amount',
        read_only=True,
    )
    is_favorited = serializers.SerializerMethodField(
        'check_is_favorited',
        read_only=True
    )

    is_in_shopping_cart = serializers.SerializerMethodField(
        'check_is_in_shopping_cart',
        read_only=True
    )

    author = UserSerializer(read_only=True)
    class Meta:
        model = Recipe
        fields = ("id", "name", "text", "cooking_time", "tags", "author", "ingredients", "image", "image_url", "is_favorited", "is_in_shopping_cart")
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.image.url)
            # return obj.image.url
        return None

    def get_ingredients_with_amount(self, obj):
        ret = []
        for val in RecipeIngredient.objects.filter(recipe=obj):
            res = {}
            res["amount"] = val.amount
            res["name"] = val.ingredient.name
            res["id"] = val.ingredient.id
            res["measurement_name"] = val.ingredient.measurement_name
            ret.append(res)
        return ret
    
    def check_is_favorited(self, obj):
        if self.context['request'].user.is_authenticated and Favorite.objects.filter(user=self.context['request'].user, recipe=obj).exists():
            return True
        return False
    
    def check_is_in_shopping_cart(self, obj):
        if self.context['request'].user.is_authenticated and ShoppingCart.objects.filter(user=self.context['request'].user, recipe=obj).exists():
            return True
        return False

    def create(self, validated_data):
        me = Recipe.objects.create(**validated_data)
        for tag_id in self.initial_data["tags"]:
            my_tag = get_object_or_404(Tag, id=tag_id)
            
            RecipeTag.objects.create(recipe = me, tag = my_tag)

        for ingredient in self.initial_data["ingredients"]:
            ingredient_id = ingredient["id"]
            ingredient_amount = ingredient["amount"]
            my_ingredient = get_object_or_404(Ingredient, id=ingredient_id)
            
            RecipeIngredient.objects.create(recipe = me, ingredient = my_ingredient, amount = ingredient_amount)

        return me
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get('cooking_time', instance.cooking_time)

        RecipeTag.objects.filter(recipe=instance).delete()
        for tag_id in self.initial_data["tags"]:
            my_tag = get_object_or_404(Tag, id=tag_id)
            
            RecipeTag.objects.create(recipe = instance, tag = my_tag)

        RecipeIngredient.objects.filter(recipe=instance).delete()
        for ingredient in self.initial_data["ingredients"]:
            ingredient_id = ingredient["id"]
            ingredient_amount = ingredient["amount"]
            my_ingredient = get_object_or_404(Ingredient, id=ingredient_id)
            
            
            RecipeIngredient.objects.create(recipe = instance, ingredient = my_ingredient, amount = ingredient_amount)

        instance.save()
        return instance
