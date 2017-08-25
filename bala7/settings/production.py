# settings/local.py
from .base import *

DEBUG = False

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_secret('PRODUCTION_DB_NAME'),
        'USER': get_secret('PRODUCTION_DB_USER'),
        'PASSWORD': get_secret('PRODUCTION_DB_PASSWORD'),
        'HOST': get_secret('PRODUCTION_DB_HOST'),
    }
}
