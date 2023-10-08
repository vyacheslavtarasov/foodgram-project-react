# Generated by Django 3.2.3 on 2023-10-03 12:23

import django.core.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0006_auto_20231002_1920"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="email",
            field=models.EmailField(
                max_length=254, unique=True, verbose_name="email address"
            ),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="first_name",
            field=models.CharField(
                default=django.utils.timezone.now, max_length=150
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="customuser",
            name="last_name",
            field=models.CharField(
                default=django.utils.timezone.now, max_length=150
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="customuser",
            name="password",
            field=models.CharField(
                max_length=150, verbose_name="User password"
            ),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="username",
            field=models.CharField(
                max_length=150,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        message="This field must contain digits and characters including @/./+/-/_.",
                        regex="^[\\w.@+-]+\\Z",
                    )
                ],
                verbose_name="Username",
            ),
        ),
        migrations.AlterField(
            model_name="tag",
            name="color",
            field=models.CharField(
                max_length=16,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        message="This field must represent a color in #XXXXXX format.",
                        regex="^#(?:[0-9a-fA-F]{3}){1,2}$",
                    )
                ],
                verbose_name="Color",
            ),
        ),
        migrations.AlterField(
            model_name="tag",
            name="slug",
            field=models.SlugField(
                max_length=200,
                null=True,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        message="This field must represent a color in #XXXXXX format.",
                        regex="^[-a-zA-Z0-9_]+$",
                    )
                ],
                verbose_name="Slug of the tag name",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="favorite",
            unique_together={("user", "recipe")},
        ),
        migrations.AlterUniqueTogether(
            name="recipeingredient",
            unique_together={("recipe", "ingredient")},
        ),
        migrations.AlterUniqueTogether(
            name="recipetag",
            unique_together={("recipe", "tag")},
        ),
        migrations.AlterUniqueTogether(
            name="shoppingcart",
            unique_together={("user", "recipe")},
        ),
        migrations.AlterUniqueTogether(
            name="subscribe",
            unique_together={("user", "user_subscribed_on")},
        ),
    ]
