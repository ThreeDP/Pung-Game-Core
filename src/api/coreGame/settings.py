import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-g8arj2c5r=vsn2=4wxkb@_ophl2shy)*#a^1aka3y4s8!z4e18'

WSGI_APPLICATION = 'coreGame.wsgi.application'
ASGI_APPLICATION = 'coreGame.asgi.application'

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'game',
    "corsheaders",
    'channels',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["DELETE", "GET", "OPTIONS", "PATCH", "POST", "PUT"]
CORS_ALLOW_HEADERS = ["*"]

ROOT_URLCONF = 'coreGame.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [(os.environ.get("REDIS_HOST", "localhost"), int(os.environ.get("REDIS_PORT", 6379)))],
        },
    },
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'GAME_CORE_DB'),
        'USER': os.environ.get('DB_USER', 'db_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'example'),
        'HOST': os.environ.get('DB_HOST', '0.0.0.0'),  # Endereço do servidor de banco de dados
        #'PORT': os.environ.get('DB_PORT', '5432'),     # Porta padrão do PostgreSQL
    }
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {name} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',  # Captura todos os níveis
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Garante que a saída seja o terminal padrão
            'formatter': 'verbose',  # Formato detalhado
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',  # Captura todos os níveis do Django
            'propagate': True,
        },
        '': {  # Logger raiz captura todos os logs, incluindo bibliotecas externas
            'handlers': ['console'],
            'level': 'DEBUG',  # Captura todos os níveis
            'propagate': False,
        },
    },
}