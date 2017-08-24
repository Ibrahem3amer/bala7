# settings/local.py
from .base import *

DEBUG = False

ALLOWED_HOSTS += ("www.najibaa.com")

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'najiba_prod_db',
        'USER': 'najiba_prod',
        'PASSWORD': '01092053058',
        'HOST': 'localhost',
        'PORT': '',
    }
}
