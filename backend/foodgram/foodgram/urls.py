from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from user.views import CustomUserViewSet

users = routers.DefaultRouter()
users.register("users", CustomUserViewSet, basename="users")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("api.urls", namespace="api")),
    path("", include("recipe.urls", namespace="recipe")),
    path("", include("user.urls", namespace="user")),
]
