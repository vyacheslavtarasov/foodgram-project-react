from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from api.views import CustomUserViewSet

users = routers.DefaultRouter()
users.register("users", CustomUserViewSet, basename='users')

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("api.urls", namespace="api")),
    path('api/', include(users.urls)),
    path("api/", include("djoser.urls")),
    path("api/auth/", include("djoser.urls.authtoken")),
]
