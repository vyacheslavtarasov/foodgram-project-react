from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    RegexValidator,
)
from django.db import models

from foodgram.constans import RecipeModelsConstants
from user.models import CustomUser


class Ingredient(models.Model):
    """Ingredient model"""

    name = models.CharField(
        verbose_name="Ingredient name",
        max_length=RecipeModelsConstants.NAME_LENGTH.value,
    )
    measurement_name = models.CharField(
        verbose_name="Unit of measure",
        max_length=RecipeModelsConstants.NAME_LENGTH.value,
    )

    class Meta:
        verbose_name = "Ingredient"
        unique_together = (("name", "measurement_name"),)
        verbose_name_plural = "Ingredients"
        ordering = ["id"]

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Tag"""

    name = models.CharField(
        verbose_name="Tag", max_length=RecipeModelsConstants.NAME_LENGTH.value
    )
    slug = models.SlugField(
        verbose_name="Slug of the tag name",
        unique=True,
        null=True,
        max_length=RecipeModelsConstants.SLUG_LENGTH.value,
        validators=[
            RegexValidator(
                regex="^[-a-zA-Z0-9_]+$",
                message="This field must represent a color in #XXXXXX format.",
            ),
        ],
    )
    color = models.CharField(
        max_length=16,
        verbose_name="Color",
        unique=True,
        validators=[
            RegexValidator(
                regex="^#(?:[0-9a-fA-F]{3}){1,2}$",
                message="This field must represent a color in #XXXXXX format.",
            ),
        ],
    )

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ["id"]

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Recipe model"""

    name = models.CharField(
        verbose_name="Recipe name",
        max_length=RecipeModelsConstants.NAME_LENGTH.value,
    )
    text = models.CharField(
        verbose_name="Recipe description",
        max_length=RecipeModelsConstants.TEXT_SMALL.value,
    )
    tags = models.ManyToManyField(Tag, through="RecipeTag")

    author = models.ForeignKey(
        CustomUser,
        related_name="recepies",
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Recipe author",
    )
    ingredients = models.ManyToManyField(
        Ingredient, through="RecipeIngredient"
    )
    cooking_time = models.SmallIntegerField(
        validators=[
            MinValueValidator(
                RecipeModelsConstants.COOCKING_TIME_MIN_VALUE.value
            ),
            MaxValueValidator(
                RecipeModelsConstants.COOCKING_TIME_MAX_VALE.value
            ),
        ]
    )
    is_favorited = models.BooleanField()
    is_in_shopping_cart = models.BooleanField()
    image = models.ImageField(
        upload_to="recipes/images/", null=True, default=None
    )

    class Meta:
        verbose_name = "Recipe"
        verbose_name_plural = "Recipes"
        ordering = ["-id"]

    def __str__(self):
        return self.name


class RecipeTag(models.Model):
    """RecipeTag model"""

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Recipe Tag"
        verbose_name_plural = "Recipe's Tags"
        unique_together = (("recipe", "tag"),)
        ordering = ["id"]

    def __str__(self):
        return f"{self.recipe} {self.tag}"


class RecipeIngredient(models.Model):
    """RecipeIngredient model"""

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.SmallIntegerField(
        validators=[
            MinValueValidator(
                RecipeModelsConstants.INGREDIENT_MIN_AMOUNT.value
            ),
            MaxValueValidator(
                RecipeModelsConstants.INGREDIENT_MAX_AMOUNT.value
            ),
        ]
    )

    class Meta:
        verbose_name = "Recipe Ingredient"
        verbose_name_plural = "Recipe's Ingredients"
        unique_together = (("recipe", "ingredient"),)
        ordering = ["id"]

    def __str__(self):
        return f"{self.recipe} {self.ingredient}"


class AbstractModel(models.Model):
    user = models.ForeignKey(
        CustomUser,
        null=True,
        on_delete=models.SET_NULL,
    )
    recipe = models.ForeignKey(Recipe, null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True
        unique_together = (("user", "recipe"),)
        ordering = ["id"]


class Favorite(AbstractModel):
    """Favorite model"""

    class Meta(AbstractModel.Meta):
        verbose_name = "Favorite"
        verbose_name_plural = "Favorites"
        default_related_name = "favorites"

    def __str__(self):
        return f"{self.user} {self.recipe}"


class ShoppingCart(AbstractModel):
    """ShoppingCart model"""

    class Meta(AbstractModel.Meta):
        verbose_name = "Shopping Cart"
        verbose_name_plural = "Shopping Carts"
        default_related_name = "shopping_carts"

    def __str__(self):
        return f"{self.user} {self.recipe}"
