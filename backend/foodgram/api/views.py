from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import AllowAny

from api.filters import IngredientFilter
from recipe.models import Ingredient, Tag
from recipe.serializers import IngredientSerializer, TagSerializer


class TagViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    Get all Tags.
    """

    pagination_class = None
    permission_classes = [AllowAny]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = "id"


class IngredientViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    Get all Ingredients.
    """

    pagination_class = None
    permission_classes = [AllowAny]
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filterset_class = IngredientFilter

    search_fields = ["name"]

    lookup_field = "id"
    search_fields = ("name",)
