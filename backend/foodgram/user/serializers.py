from rest_framework import serializers

from api.models import (
    CustomUser,
    Subscribe,
)


class UserSerializer(serializers.ModelSerializer):
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
