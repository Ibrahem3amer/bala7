# settings/ci.py
from .base import *

DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'travis_ci_test',
        'USER': 'postgres'
    }
}
MIDDLEWARE += ("debug_toolbar.middleware.DebugToolbarMiddleware", )

INSTALLED_APPS += ("debug_toolbar", "django_extensions")
