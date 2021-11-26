# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
from .base import *

DEBUG = config('DEBUG')
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': config('DB_HOST'),  # env
        'NAME': config('DB_NAME'),  # env
        'USER': config('DB_USER'),  # env
        'PASSWORD': config('DB_PWD'),  # env
        'PORT': config('DB_PORT')  # env
    }
}
STATICFILES_DIRS = (BASE_DIR.parent / 'static',)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
}


