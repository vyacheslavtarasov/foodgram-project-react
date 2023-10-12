from django.urls import include, path
from rest_framework import routers

from api.views import IngredientViewSet, TagViewSet

app_name = "api"

router = routers.DefaultRouter(trailing_slash=True)

router.register(r"ingredients", IngredientViewSet, basename="ingredients")
router.register(r"tags", TagViewSet, basename="tags")

urlpatterns = [
    path("api/", include(router.urls)),
]
