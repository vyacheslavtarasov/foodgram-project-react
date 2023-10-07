import psycopg2

import os
from dotenv import load_dotenv
import json
load_dotenv()
from django.core.management.base import BaseCommand

database = os.getenv("POSTGRES_DB", "django")
user = os.getenv("POSTGRES_USER", "django")
password = os.getenv("POSTGRES_PASSWORD", "")
host = os.getenv("DB_HOST", "")
port = os.getenv("DB_PORT", "5432")

tag_data = [["завтрак", "breakfast", "#111111"], ["обед", "dinner", "#222222"], ["ужин", "supper", "#333333"]]


class Command(BaseCommand):
    help = "Import data from local csv files into database."

    def handle(self, *args, **kwargs):

        self.stdout.write("Ready to import data for 'Ingredient' and 'Tag' tables.")

        conn = psycopg2.connect(database=database, 
                                user=user, password=password,  
                                host=host, port=int(port)
        ) 
        
        conn.autocommit = True
        cursor = conn.cursor()

        sql = ''' DELETE FROM api_ingredient;'''

        cursor.execute(sql) 

        sql = ''' DELETE FROM api_tag;'''

        cursor.execute(sql)

        
        dictionary_list = []
        with open('/app/foodgram/data/ingredients.json', encoding='utf-8') as json_file:
            dictionary_list = json.load(json_file)

        for d in dictionary_list:
            cursor.execute("INSERT INTO api_ingredient (name, measurement_name) VALUES (%s, %s)", (d["name"], d["measurement_unit"]))

        for data in tag_data:
            cursor.execute("INSERT INTO api_tag (name, slug, color) VALUES (%s, %s, %s)", (data[0], data[1], data[2]))

        conn.commit()
        conn.close()

        self.stdout.write("Import Complete!")

