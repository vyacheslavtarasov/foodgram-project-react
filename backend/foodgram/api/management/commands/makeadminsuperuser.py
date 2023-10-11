import os

from django.core.management.base import BaseCommand
from dotenv import load_dotenv

from api.models import CustomUser

load_dotenv()


def createSuperUser(username, password, email="", firstName="", lastName=""):
    invalidInputs = ["", None]

    if username.strip() in invalidInputs or password.strip() in invalidInputs:
        return None

    user = CustomUser(
        username=username,
        email=email,
        first_name=firstName,
        last_name=lastName,
    )
    user.set_password(password)
    user.is_superuser = True
    user.is_staff = True
    user.save()

    return user


class Command(BaseCommand):
    help = "Create superuser by the name of admin"

    def handle(self, *args, **kwargs):
        createSuperUser(
            "admin", "admin123admin", "admin@admin.ru", "admin", "admin"
        )
