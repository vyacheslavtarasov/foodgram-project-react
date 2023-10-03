import django_filters

from .models import Recipe


class RecipeFilter(django_filters.FilterSet):

    # name = django_filters.CharFilter()
    author = django_filters.CharFilter(lookup_expr='id')
    tags = django_filters.MultipleChoiceFilter(lookup_expr='slug')
    is_favorited = django_filters.BooleanFilter()

    class Meta:
        model = Recipe
        fields = ['name', 'author', 'tags', 'is_favorited']