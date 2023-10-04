import django_filters

from .models import Recipe
from api.models import Ingredient, Tag, CustomUser, Recipe, RecipeTag, RecipeIngredient, Favorite, ShoppingCart, Subscribe

STATUS_CHOICES = (
    (0, False),
    (1, True),
)

def get_tag_choises():
    tags = Tag.objects.all()
    choices = [(tag.slug, tag.slug) for tag in tags]
    return choices

class RecipeFilter(django_filters.FilterSet):

    author = django_filters.CharFilter(lookup_expr='id')
    tags = django_filters.MultipleChoiceFilter(choices=get_tag_choises, lookup_expr='slug')
    is_in_shopping_cart = django_filters.ChoiceFilter(choices=STATUS_CHOICES, field_name='is_in_shopping_cart', method='filter_shopping_cart')
    is_favorited = django_filters.ChoiceFilter(choices=STATUS_CHOICES, field_name='is_favorited', method='filter_favorite')

    def filter_shopping_cart(self, queryset, name, value):
        goods = ShoppingCart.objects.all()
        if value == "1":
            goods = goods.filter(user=self.request.user)
        elif value == "0":
            goods = goods.exclude(user=self.request.user)
        recipes = []
        [recipes.append(i.recipe.id) for i in goods]
        ret = queryset.filter(id__in=recipes)
        return ret
    
    def filter_favorite(self, queryset, name, value):
        goods = Favorite.objects.all()
        if value == "1":
            goods = goods.filter(user=self.request.user)
        elif value == "0":
            goods = goods.exclude(user=self.request.user)
        recipes = []
        [recipes.append(i.recipe.id) for i in goods]
        ret = queryset.filter(id__in=recipes)
        return ret


    class Meta:
        model = Recipe
        fields = ['name', 'author', 'tags', 'is_favorited', 'is_in_shopping_cart']