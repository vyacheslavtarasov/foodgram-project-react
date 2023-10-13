from django.urls import include, path
from rest_framework import routers

from user.views import CustomUserViewSet

app_name = "user"

router = routers.DefaultRouter(trailing_slash=True)

users = routers.DefaultRouter()
users.register("users", CustomUserViewSet, basename="users")

urlpatterns = [
    path("", include(users.urls)),
    path("", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
]
