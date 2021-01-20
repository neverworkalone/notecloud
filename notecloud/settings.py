"""
Django settings for notecloud project.

Generated by 'django-admin startproject' using Django 3.0.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import json
import os
import sys

from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')
TEMPLATES_DIR = os.path.join(FRONTEND_DIR, 'templates')

TEST_SETTING = False
if 'DJANGO_SETTINGS_MODULE' in os.environ:
    if os.environ['DJANGO_SETTINGS_MODULE'] == 'tests.test_settings':
        TEST_SETTING = True


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRETS_PATH = 'secrets.json'
CONFIG_PATH = 'config.json'

if TEST_SETTING:
    SECRETS_PATH = 'tests/test_secrets.json'
    CONFIG_PATH = 'tests/test_config.json'


# Load sensitive data from SECRETS_PATH. (secrets.json)
# Do not change below, edit your own secrets.json instead.
# See tests/test_secrets.json

try:
    secrets = json.loads(open(os.path.join(BASE_DIR, SECRETS_PATH)).read())

    DB_HOST = ''
    DB_PORT = ''
    DB_NAME = ''
    DB_USER = ''
    DB_PASSWORD = ''
    EMAIL_HOST = ''
    EMAIL_PORT = 25
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''
    EMAIL_ADDRESS = ''
    AWS_ACCESS_KEY_ID = ''
    AWS_SECRET_ACCESS_KEY = ''
    SECRET_KEY = ''
    # DO NOT COMMIT YOUR SECRETS ABOVE INTO PUBLIC REPOSITORY.

    for key, value in secrets.items():
        setattr(sys.modules[__name__], key, value)
except IOError:
    raise IOError('Error while loading %s.' % SECRETS_PATH)


# Default configurations.
# It is highly suggested to override in CONFIG_PATH to change configurations.
# See tests/test_config.json

SITE_NAME = 'Notecloud'
FRONTEND_URL = 'http://127.0.0.1:8080'
DEFAULT_FROM_EMAIL = EMAIL_ADDRESS
DATABASE_ENGINE = 'django.db.backends.postgresql'
DEBUG = False
LOCAL_SERVER = False
TRACE_ENABLED = False
REST_PAGINATION_SIZE_DEFAULT = 20
DATE_TIME_FORMAT_DEFAULT = '%Y-%m-%dT%H:%M:%S%z'
DATE_FORMAT_DEFAULT = '%Y-%m-%d'
DO_NOT_SEND_EMAIL = False
FIRST_WEEKDAY_SUNDAY = True  # Monday if False

# Load project configuration from CONFIG_PATH if exist. (config.json)
try:
    config = json.loads(open(os.path.join(BASE_DIR, CONFIG_PATH)).read())
    print("# Override configurations.")

    for key, value in config.items():
        setattr(sys.modules[__name__], key, value)
        print(" %s : %s" % (key, value))
except IOError:
    pass


# Security
# https://docs.djangoproject.com/en/3.1/topics/security/

if not LOCAL_SERVER:
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    CSRF_COOKIE_SECURE = True

ALLOWED_HOSTS = ['*']


# CORS headers
# https://github.com/adamchainz/django-cors-headers

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    FRONTEND_URL,
]


# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
THIRD_PARTY_APPS = [
    'corsheaders',
    'drf_yasg',
    'rest_framework',
    'rest_framework.authtoken',
]
LOCAL_APPS = [
    'accounts',
    'frontend',
    'notes',
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'notecloud.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            TEMPLATES_DIR,
        ],
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

WSGI_APPLICATION = 'notecloud.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': DATABASE_ENGINE,
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
        'TEST': {
            'NAME': DB_NAME,
        },
    }
}


# Substituting a custom User model
# https://docs.djangoproject.com/en/3.1/topics/auth/customizing/

AUTH_USER_MODEL = 'accounts.User'


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
]
if LOCAL_SERVER and not TEST_SETTING:
    AUTH_PASSWORD_VALIDATORS = []


# Rest framework
# https://github.com/encode/django-rest-framework

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'core.pagination.PageNumberPagination',
    'PAGE_SIZE': REST_PAGINATION_SIZE_DEFAULT,
    'DATETIME_FORMAT': DATE_TIME_FORMAT_DEFAULT,
    'DATE_FORMAT': DATE_FORMAT_DEFAULT,
}


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

LANGUAGES = [
    ('ko-kr', _('Korean')),
    ('en-us', _('English')),
]
LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(FRONTEND_DIR, 'static'),
)

# Static files on AWS S3
# https://github.com/jschneier/django-storages
# AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY should be set in SECRETS_PATH

if 'storages' in INSTALLED_APPS and not LOCAL_SERVER:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_QUERYSTRING_AUTH = False
    AWS_DEFAULT_ACL = 'public-read'
    AWS_DOMAIN = '.s3.ap-northeast-2.amazonaws.com'
    AWS_STORAGE_BUCKET_NAME = 'media'
    AWS_S3_CUSTOM_DOMAIN = AWS_STORAGE_BUCKET_NAME + AWS_DOMAIN
    AWS_QUERYSTRING_AUTH = False
    AWS_DEFAULT_ACL = 'public-read'
    MEDIA_URL = 'https://' + AWS_S3_CUSTOM_DOMAIN + '/'
else:
    MEDIA_URL = '/upload/'
MEDIA_ROOT = os.path.join(FRONTEND_DIR, 'upload')


# Logging
# https://docs.djangoproject.com/en/3.1/topics/logging/

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'notecloud.trace': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    },
}
