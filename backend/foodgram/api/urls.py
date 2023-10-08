from django.urls import include, path
from rest_framework import routers

from api.views import (IngredientViewSet, RecipeViewSet, TagViewSet,
                       api_download_shopping_cart, api_favorite,
                       api_shopping_cart, api_subscribe, api_subscriptions)

app_name = "api"

router = routers.DefaultRouter(trailing_slash=True)

router.register(r"recipes", RecipeViewSet, basename="recipes")
router.register(r"ingredients", IngredientViewSet, basename="ingredients")
router.register(r"tags", TagViewSet, basename="tags")

urlpatterns = [
    path("api/users/subscriptions/", api_subscriptions),
    path("api/users/<int:id>/subscribe/", api_subscribe),
    path("api/recipes/<int:id>/favorite/", api_favorite),
    path("api/recipes/<int:id>/shopping_cart/", api_shopping_cart),
    path("api/recipes/download_shopping_cart/", api_download_shopping_cart),
    path("api/", include(router.urls)),
]
