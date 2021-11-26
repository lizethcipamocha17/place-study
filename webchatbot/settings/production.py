from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': config('DB_HOST'),  # env
        'NAME': config('DB_NAME'),  # env
        'USER': config('DB_USER'),  # env
        'PASSWORD': config('DB_PWD'),  # env
        'PORT': config('DB_PORT')  # env
    }
}

STATIC_ROOT = BASE_DIR.parent / 'static'
