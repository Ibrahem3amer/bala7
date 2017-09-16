# settings/local.py
from .base import *

DEBUG = False

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_BROWSER_XSS_FILTER = True

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

CSRF_COOKIE_HTTPONLY = True

X_FRAME_OPTIONS = 'DENY'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_secret('PRODUCTION_DB_NAME'),
        'USER': get_secret('PRODUCTION_DB_USER'),
        'PASSWORD': get_secret('PRODUCTION_DB_PASSWORD'),
        'HOST': get_secret('PRODUCTION_DB_HOST'),
    }
}

SESSION_ENGIN = 'django.contrib.sessions.backends.cached_db'
