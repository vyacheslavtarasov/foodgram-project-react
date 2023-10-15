import json

from django.core.management.base import BaseCommand

from recipe.models import Ingredient, Tag

tag_data = [
    {"name": "завтрак", "slug": "breakfast", "color": "#111111"},
    {"name": "обед", "slug": "dinner", "color": "#222222"},
    {"name": "ужин", "slug": "supper", "color": "#333333"},
]


class Command(BaseCommand):
    help = "Import data from local csv files into database."

    def handle(self, *args, **kwargs):
        self.stdout.write(
            "Ready to import data for 'Ingredient' and 'Tag' tables."
        )

        with open("data/ingredients.json", encoding="utf-8") as json_file:
            dictionary_list = json.load(json_file)

        Ingredient.objects.all().delete()

        ingredient_list = [
            Ingredient(name=d["name"], measurement_unit=d["measurement_unit"])
            for d in dictionary_list
        ]

        Ingredient.objects.bulk_create(ingredient_list)

        Tag.objects.all().delete()
        for data in tag_data:
            Tag.objects.get_or_create(**data)

        self.stdout.write("Import Complete!")
