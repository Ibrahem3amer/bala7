import os
import json
from django.core.exceptions import ImproperlyConfigured

path = os.path.dirname(__file__)+'/secrets.json'
with open(path) as f:
	secrets = json.loads(f.read())

def get_secret(var_name):
	"""Get the environment variable or return exception."""
	try:
		return secrets[var_name]
	except KeyError:
		error_msg = "Set the {} environment variable".format(var_name)
		raise ImproperlyConfigured(error_msg)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret('SECRET_KEY')


ALLOWED_HOSTS = get_secret('ALLOWED_HOSTS')


# Application definition

INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'users',
	'cms',
	'social_django',
	'rest_framework',
]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bala7.urls'

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
				# Social auth
				'social_django.context_processors.backends',
				'social_django.context_processors.login_redirect',
				# User nav topics
				'users.context_processors.add_nav_topics'
			],
		},
	},
]

WSGI_APPLICATION = 'bala7.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
	{
		'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
	},
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/home/najiba/static'

# Media files
ENV_PATH    = os.path.abspath(os.path.dirname(__file__))
MEDIA_ROOT  = os.path.join(BASE_DIR, 'media/')
MEDIA_URL   = "media/"

# Auth backend settings - Social auth
AUTHENTICATION_BACKENDS = [
	'social_core.backends.twitter.TwitterOAuth',
	'social_core.backends.facebook.FacebookOAuth2',
	'django.contrib.auth.backends.ModelBackend',
]

# URL that redirected to after logout, unauthorized page.
LOGIN_REDIRECT_URl  = '/'
LOGIN_URL           = '/users/login'

# Social media auth pipline settings
SOCIAL_AUTH_PIPELINE = [
	'social_core.pipeline.social_auth.social_details',
	'social_core.pipeline.social_auth.social_uid',
	'social_core.pipeline.social_auth.social_user',
	'social_core.pipeline.user.get_username',
	'social_core.pipeline.user.create_user',
	'social_core.pipeline.social_auth.associate_user',
	'social_core.pipeline.social_auth.load_extra_data',
	'social_core.pipeline.user.user_details',
	'social_core.pipeline.social_auth.associate_by_email',
	'users.models.make_social_new_profile',
]

# Storing user choises when completing with social.
SOCIAL_AUTH_FIELDS_STORED_IN_SESSION = ['first_form_data']

# Facebook auth settings
SOCIAL_AUTH_FACEBOOK_KEY = '1907562042790610'
SOCIAL_AUTH_FACEBOOK_SECRET = get_secret('FACEBOOK_SECRET')
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
'fields': 'id, name, email, age_range'
}

# Twiiter auth settings
SOCIAL_AUTH_TWITTER_KEY = 'lHt8gjwWyvYWSkEdxkSc5C2C8'
SOCIAL_AUTH_TWITTER_SECRET = get_secret('TWITTER_SECRET')