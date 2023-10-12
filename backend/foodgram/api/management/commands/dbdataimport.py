import json

from django.core.management.base import BaseCommand
from api.models import (Ingredient, Tag)

tag_data = [
    ["завтрак", "breakfast", "#111111"],
    ["обед", "dinner", "#222222"],
    ["ужин", "supper", "#333333"],
]


class Command(BaseCommand):
    help = "Import data from local csv files into database."

    def handle(self, *args, **kwargs):
        self.stdout.write(
            "Ready to import data for 'Ingredient' and 'Tag' tables."
        )

        dictionary_list = []
        with open(
            "/app/foodgram/data/ingredients.json", encoding="utf-8"
            # "data/ingredients.json", encoding="utf-8"

        ) as json_file:
            dictionary_list = json.load(json_file)
        
        Ingredient.objects.all().delete()

        ingredient_list = [Ingredient(name=d["name"], measurement_name=d["measurement_unit"]) for d in dictionary_list]

        Ingredient.objects.bulk_create(ingredient_list)

        Tag.objects.all().delete()
        for data in tag_data:
            Tag.objects.get_or_create(name=data[0], slug=data[1], color=data[2])

        self.stdout.write("Import Complete!")
