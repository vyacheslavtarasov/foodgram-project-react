from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

app_name = "user"

router = routers.DefaultRouter(trailing_slash=True)

from user.views import CustomUserViewSet

users = routers.DefaultRouter()
users.register("users", CustomUserViewSet, basename='users')

urlpatterns = [
    path('api/', include(users.urls)),
    path("api/", include("djoser.urls")),
    path("api/auth/", include("djoser.urls.authtoken")),
]