from django.urls import include, path
from rest_framework import routers

from api.views import TagViewSet, IngredientViewSet, RecipeViewSet, api_favorite, api_subscriptions, api_subscribe
app_name = "api"

router = routers.DefaultRouter(trailing_slash=True)

router.register(r"recipes", RecipeViewSet, basename="recipes")
router.register(r"ingredients", IngredientViewSet, basename="ingredients")
router.register(r"tags", TagViewSet, basename="tags")

urlpatterns = [
    
    path('api/users/<int:id>/subscribe', api_subscribe),
    path('api/recipes/<int:id>/favorite/', api_favorite),
    path("api/", include(router.urls)),
    path('api/users/subscriptions', api_subscriptions),
    
]