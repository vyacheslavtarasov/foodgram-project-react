from rest_framework import serializers

from recipe.models import CustomUser, Recipe

from user.models import Subscribe


class UserSerializer4Djoser(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_subscribed = serializers.SerializerMethodField(
        "check_is_subscribed", read_only=True
    )

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "id",
            "password",
            "email",
            "last_name",
            "first_name",
            "is_subscribed",
        ]

    def check_is_subscribed(self, obj):
        current_user = self.context["request"].user
        return (
            current_user.is_authenticated
            and Subscribe.objects.filter(
                user=self.context["request"].user, user_subscribed_on=obj
            ).exists()
        )


class UserSerializer(UserSerializer4Djoser):
    recipes = serializers.SerializerMethodField(
        "get_recipes",
        read_only=True,
    )

    recipes_count = serializers.SerializerMethodField(
        "get_recipes_count",
        read_only=True,
    )

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "id",
            "password",
            "email",
            "last_name",
            "first_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        ]

    def get_recipes(self, obj):
        recipes_limit = None
        if "recipes_limit" in self.context:
            recipes_limit = self.context["recipes_limit"]
        recipes = Recipe.objects.filter(author=obj)
        ret = []
        for idx, recipe in enumerate(recipes):
            ret.append(
                {
                    "id": recipe.id,
                    "name": recipe.name,
                    "cooking_time": recipe.cooking_time,
                    "image": recipe.image.url,
                }
            )
            if recipes_limit and idx > recipes_limit:
                break
        return ret

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = "__all__"
