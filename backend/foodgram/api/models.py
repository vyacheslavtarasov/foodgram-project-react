from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Модель переопределенного юзера."""

    username = models.CharField(
        'Имя пользователя',
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
        "Пароль пользователя",
        max_length=100, null=True
    )

    REQUIRED_FIELDS = ["username", "first_name", "last_name", "password"]
    USERNAME_FIELD = "email"

    def __str__(self):
        return str(self.username)

class Ingredients(models.Model):
    """Модель ингредиентов.
    Один ингредиент может принадлежать нескольким рецептам.
    Одни рецепт может содержать несколько ингредиентов."""

    name = models.CharField(verbose_name="Название ингредиента", max_length=200)
    measurement_name = models.CharField(verbose_name="Единица измерения", max_length=200)

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        ordering = ["id"]

    def __str__(self):
        return self.name
    
class Tag(models.Model):
    """Тег"""

    name = models.CharField(verbose_name="Название тега", max_length=200)
    slug = models.SlugField(
        verbose_name="Slug названия тега",
        unique=True
    )
    color = models.CharField(max_length=16)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ["id"]

    def __str__(self):
        return self.name
    
class Recipe(models.Model):
    """Рецепт"""

    name = models.CharField(verbose_name="Название рецепта", max_length=200)
    text = models.CharField(verbose_name="Описание рецепта.", max_length=200)
    tags = models.ManyToManyField(Tag, through="RecipeTag")

    author = models.ForeignKey(
        CustomUser, related_name='recepies', null=True,
        on_delete=models.SET_NULL
    )
    ingredients = models.ManyToManyField(Ingredients, through="RecipeIngredient")
    cooking_time = models.IntegerField()
    is_favorited = models.BooleanField()
    is_in_shopping_cart = models.BooleanField()
    image = models.ImageField(
        upload_to='recipes/images/',
        null=True,
        default=None
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ["id"]

    def __str__(self):
        return self.name
    
class RecipeTag(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.recipe} {self.tag}'

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return f'{self.recipe} {self.ingredient}'
    
class Favorite(models.Model):
    user = models.ForeignKey(
        CustomUser, related_name='custom_users', null=True,
        on_delete=models.SET_NULL
    )
    recipe = models.ForeignKey(
        Recipe, related_name='recepies', null=True,
        on_delete=models.SET_NULL
    )


class Subscribe(models.Model):
    user = models.ForeignKey(
        CustomUser, related_name='users', null=True,
        on_delete=models.SET_NULL
    )
    user_subscribed_on = models.ForeignKey(
        CustomUser, related_name='users_subscribed_on', null=True,
        on_delete=models.SET_NULL
    )

# class Achievement(models.Model):
#     name = models.CharField(max_length=64)
#     slug = models.SlugField(
#         verbose_name="Slug названия тега",
#         unique=True
#     )
#     color = models.CharField(max_length=16)

#     def __str__(self):
#         return self.name


# class Cat(models.Model):
#     name = models.CharField(max_length=16)
#     color = models.CharField(max_length=16)
#     birth_year = models.IntegerField()
#     # Связь будет описана через вспомогательную модель AchievementCat
#     achievements = models.ManyToManyField(Achievement, through='AchievementCat')
    

#     def __str__(self):
#         return self.name

# # В этой модели будут связаны id котика и id его достижения
# class AchievementCat(models.Model):
#     achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
#     cat = models.ForeignKey(Cat, on_delete=models.CASCADE)

#     def __str__(self):
#         return f'{self.achievement} {self.cat}' 