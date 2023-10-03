from datetime import date

from django.conf import settings
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError


class UsernameValidatorRegex(UnicodeUsernameValidator):
    """Username validator"""

    regex = r"^[\w.@+-]+\Z"
    flag = 0
    max_length = settings.LENG_LOGIN_USER
    message = (
        f"Enter corrent username."
        f" It must contain digits and characters including @/./+/-/_."
        f" Length must be less or equal {settings.LENG_LOGIN_USER} symbols"
    )
    error_message = {
        "invalid": f"Lenght is more than {settings.LENG_LOGIN_USER}. "
        "Only digits and characters including @/./+/-/_ are allowed",
        "required": "The field must not be empty!",
    }