# from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
# from django.db import models

# from foodgram.constans import ModelsConstants
# from api.models import Ingredient, Tag
# from user.models import CustomUser


# class Recipe(models.Model):
#     """Recipe model"""

#     name = models.CharField(verbose_name="Recipe name", max_length=ModelsConstants.NAME_LENGTH.value)
#     text = models.CharField(verbose_name="Recipe description", max_length=ModelsConstants.TEXT_SMALL.value)
#     tags = models.ManyToManyField(Tag, through="RecipeTag")

#     author = models.ForeignKey(
#         CustomUser,
#         related_name="recepies",
#         null=True,
#         on_delete=models.SET_NULL,
#         verbose_name="Recipe author",
#     )
#     ingredients = models.ManyToManyField(
#         Ingredient, through="RecipeIngredient"
#     )
#     cooking_time = models.SmallIntegerField(validators=[MinValueValidator(ModelsConstants.COOCKING_TIME_MIN_VALUE.value),
#                                        MaxValueValidator(ModelsConstants.COOCKING_TIME_MAX_VALE.value)])
#     is_favorited = models.BooleanField()
#     is_in_shopping_cart = models.BooleanField()
#     image = models.ImageField(
#         upload_to="recipes/images/", null=True, default=None
#     )

#     class Meta:
#         verbose_name = "Recipe"
#         verbose_name_plural = "Recipes"
#         ordering = ["-id"]

#     def __str__(self):
#         return self.name