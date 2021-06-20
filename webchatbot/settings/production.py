
from .base import *

DEBUG = config('DEBUG')
# DEBUG = True
ALLOWED_HOSTS = ['https://djangoapichatbot.herokuapp.com/']

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
