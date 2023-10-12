from django.urls import include, path
from rest_framework import routers

from recipe.views import (RecipeViewSet)

app_name = "recipe"

router = routers.DefaultRouter(trailing_slash=True)

router.register(r"recipes", RecipeViewSet, basename="recipes")

urlpatterns = [
    path("api/", include(router.urls)),
]