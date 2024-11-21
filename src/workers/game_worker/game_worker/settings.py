import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "channels",
    "gamessesion",
]

MIDDLEWARE = []

ROOT_URLCONF = None

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "GAME_CORE_DB"),
        "USER": os.environ.get("DB_USER", "db_user"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "example"),
        "HOST": os.environ.get("DB_HOST", "0.0.0.0"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = False
USE_TZ = False

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Configuração do Django Channels com Redis
ASGI_APPLICATION = "game_worker.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(os.environ.get("REDIS_HOST", "localhost"), int(os.environ.get("REDIS_PORT", 6379)))],
        },
    },
}