from config.settings.base import *

SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")

ALLOWED_HOSTS = str(env("ALLOWED_HOSTS")).split(",")

API_TOKEN = env("API_TOKEN")

EXTERNAL_APPS = ["rest_framework", "django.contrib.humanize", "drf_yasg"]
LOCAL_APPS = ["src.core", "src.documents"]

INSTALLED_APPS += EXTERNAL_APPS + LOCAL_APPS

AUTH_USER_MODEL = "core.CustomUser"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": 5432
    }
}

TIME_ZONE = "Asia/Tashkent"

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, "asserts")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

# message
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-secondary',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ],
    'COERCE_DECIMAL_TO_STRING': False,
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}