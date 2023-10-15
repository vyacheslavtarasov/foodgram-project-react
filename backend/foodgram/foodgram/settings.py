import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-cg6*%6d51ef8f#4!r3*$pmxm4)abgjw8mo!4y-q*uq1!4$-89$",
)

DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "api.apps.ApiConfig",
    "user.apps.UserConfig",
    "recipe.apps.RecipeConfig",
    "rest_framework",
    "djoser",
    "rest_framework.authtoken",
    "django_filters",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "foodgram.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "foodgram.wsgi.application"

AUTH_USER_MODEL = "user.CustomUser"

DJOSER = {
    "HIDE_USERS": False,
    "PERMISSIONS": {
        "user_list": ["rest_framework.permissions.AllowAny"],
        "user": ["rest_framework.permissions.IsAuthenticated"],
    },
    "SERIALIZERS": {
        "user": "user.serializers.UserSerializer4Djoser",
        "current_user": "user.serializers.UserSerializer4Djoser",
    },
}

REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend"
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "api.paginations.CustomPagination",
    "PAGE_SIZE": 2,
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "django"),
        "USER": os.getenv("POSTGRES_USER", "django"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", ""),
        "HOST": os.getenv("DB_HOST", ""),
        "PORT": os.getenv("DB_PORT", 5432),
    }
}

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "djangoapp.log",
        },
        "file2": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "djangoapp2.log",
        },
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True,
        },
        'django.request': {
            'handlers': ["file2"],
            'level': 'INFO',  # change debug level as appropiate
            'propagate': False,
        },
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.NumericPasswordValidator"
        ),
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = "/backend_static/"
STATIC_ROOT = "/backend_static/"

MEDIA_URL = "/media/"
MEDIA_ROOT = "/media/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LENG_LOGIN_USER = 11
