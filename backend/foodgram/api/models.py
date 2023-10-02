from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Custom User model"""

    username = models.CharField(
        'Username',
        max_length=150,
        unique=True,
    )
    first_name = models.CharField(max_length=150, null=True)
    last_name = models.CharField(max_length=150, null=True)
    email = models.EmailField(
        blank=True,
        max_length=254,
        unique=True,
        verbose_name="email address",
    )
    password = models.CharField(
        "User password",
        max_length=100, null=True
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-id"]

    REQUIRED_FIELDS = ["username", "first_name", "last_name", "password"]
    USERNAME_FIELD = "email"

    def __str__(self):
        return str(self.username)

class Ingredient(models.Model):
    """Ingredient model"""

    name = models.CharField(verbose_name="Ingredient name", max_length=200)
    measurement_name = models.CharField(verbose_name="Unit of measure", max_length=200)

    class Meta:
        verbose_name = "Ingredient"
        verbose_name_plural = "Ingredients"
        ordering = ["id"]

    def __str__(self):
        return self.name
    
class Tag(models.Model):
    """Tag"""

    name = models.CharField(verbose_name="Tag", max_length=200)
    slug = models.SlugField(
        verbose_name="Slug of the tag name",
        unique=True
    )
    color = models.CharField(max_length=16,
        verbose_name="Color",
        unique=True
    )

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ["id"]

    def __str__(self):
        return self.name
    
class Recipe(models.Model):
    """Recipe model"""

    name = models.CharField(verbose_name="Recipe name", max_length=200)
    text = models.CharField(verbose_name="Recipe description", max_length=200)
    tags = models.ManyToManyField(Tag, through="RecipeTag")

    author = models.ForeignKey(
        CustomUser, related_name='recepies', null=True,
        on_delete=models.SET_NULL,
        verbose_name="Recipe author"
    )
    ingredients = models.ManyToManyField(Ingredient, through="RecipeIngredient")
    cooking_time = models.IntegerField()
    is_favorited = models.BooleanField()
    is_in_shopping_cart = models.BooleanField()
    image = models.ImageField(
        upload_to='recipes/images/',
        null=True,
        default=None
    )

    class Meta:
        verbose_name = "Recipe"
        verbose_name_plural = "Recipes"
        ordering = ["id"]

    def __str__(self):
        return self.name
    
class RecipeTag(models.Model):
    """RecipeTag model"""


    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Recipe Tag"
        verbose_name_plural = "Recipe's Tags"
        ordering = ["id"]

    def __str__(self):
        return f'{self.recipe} {self.tag}'

class RecipeIngredient(models.Model):
    """RecipeIngredient model"""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.IntegerField()

    class Meta:
        verbose_name = "Recipe Ingredient"
        verbose_name_plural = "Recipe's Ingredients"
        ordering = ["id"]

    def __str__(self):
        return f'{self.recipe} {self.ingredient}'
    
class Favorite(models.Model):
    """Favorite model"""


    user = models.ForeignKey(
        CustomUser, related_name='custom_users', null=True,
        on_delete=models.SET_NULL
    )
    recipe = models.ForeignKey(
        Recipe, related_name='recepies', null=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = "Favorite"
        verbose_name_plural = "Favorites"
        ordering = ["id"]

    def __str__(self):
        return f'{self.user} {self.recipe}'

class ShoppingCart(models.Model):
    """ShoppingCart model"""

    user = models.ForeignKey(
        CustomUser, related_name='shopping_cart_users', null=True,
        on_delete=models.SET_NULL
    )
    recipe = models.ForeignKey(
        Recipe, related_name='shopping_cart_recipes', null=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = "Shopping Cart"
        verbose_name_plural = "Shopping Carts"
        ordering = ["id"]

    def __str__(self):
        return f'{self.user} {self.recipe}'

class Subscribe(models.Model):
    """Subscribe model"""
    user = models.ForeignKey(
        CustomUser, related_name='users', null=True,
        on_delete=models.SET_NULL
    )
    user_subscribed_on = models.ForeignKey(
        CustomUser, related_name='users_subscribed_on', null=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = "Subscribe"
        verbose_name_plural = "Subscriptions"
        ordering = ["id"]

    def __str__(self):
        return f'{self.user} {self.user_subscribed_on}'
