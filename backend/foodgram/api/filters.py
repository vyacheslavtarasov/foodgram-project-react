import django_filters

from django_filters.widgets import BooleanWidget
from recipe.models import Favorite, Recipe, ShoppingCart, Tag


def get_tag_choices():
    tags = Tag.objects.all()
    return [(tag.slug, tag.slug) for tag in tags]


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.MultipleChoiceFilter(
        choices=get_tag_choices, lookup_expr="slug"
    )
    is_in_shopping_cart = django_filters.BooleanFilter(
        widget=BooleanWidget(),
        field_name="is_in_shopping_cart",
        method="filter_shopping_cart",
    )
    is_favorited = django_filters.BooleanFilter(
        field_name="is_favorited",
        method="filter_favorite",
        widget=BooleanWidget(),
    )

    def filter_shopping_cart(self, queryset, name, value):
        chosen = ShoppingCart.objects.filter(user=self.request.user)
        recipe_ids = [i.recipe.id for i in chosen]
        return queryset.filter(id__in=recipe_ids) if value else queryset

    def filter_favorite(self, queryset, name, value):
        favorited = Favorite.objects.filter(user=self.request.user)
        recipe_ids = [i.recipe.id for i in favorited]
        return queryset.filter(id__in=recipe_ids) if value else queryset

    class Meta:
        model = Recipe
        fields = [
            "name",
            "author",
            "tags",
            "is_favorited",
            "is_in_shopping_cart",
        ]
