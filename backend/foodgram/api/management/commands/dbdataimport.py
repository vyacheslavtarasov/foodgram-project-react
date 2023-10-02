import sqlite3

import pandas
from django import db
from django.core.management.base import BaseCommand

import_template = [
    ("ingredients", "api_ingredient"),
]


class Command(BaseCommand):
    help = "Import data from local csv files into database."

    def handle(self, *args, **kwargs):
        db_path = db.utils.settings.DATABASES["default"]["NAME"]

        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        for entry in import_template:
            (file_name, table_name) = entry

            c.execute(
                f"DELETE FROM {table_name};",
            )

            conn.commit()

        #     # давайте предположим, что файлы будут всегда лежать здесь
            df = pandas.read_csv(f"../../data/{file_name}.csv", names=["name", "measurement_name"])

            df.to_sql(table_name, conn, if_exists="append", index=False)

        conn.close()

        self.stdout.write("Import Complete!")