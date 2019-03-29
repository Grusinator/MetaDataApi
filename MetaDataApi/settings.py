"""
Django settings for MetaDataApi project.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import json
import os
import posixpath

import django_heroku

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECT_DIR = os.path.dirname(__file__)

# PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

# app/fixtures is a default fixture dir and should not be added
# FIXTURE_DIRS = (os.path.join(PROJECT_ROOT, 'fixtures'),)

# from django.core.management import call_command

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
try:
    SECRET_KEY = os.environ['SECRET_KEY']
except:
    SECRET_KEY = 'ymcvw8ej))e=9jo89315q_r$imri(u0-ae!utev&ck4rs6cz+d'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

CORS_ORIGIN_ALLOW_ALL = True

CORS_ORIGIN_WHITELIST = (
    'localhost:3000',
    'localhost:3002'
)

AUTHENTICATION_BACKENDS = [
    'graphql_jwt.backends.JSONWebTokenBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'service_objects',
    'graphene_django',
    # 'oauth2_provider',
    'corsheaders',
    'storages',
    'admin_reorder',
    'graphene_file_upload',
    'MetaDataApi.users',
    'MetaDataApi.datapoints',
    'MetaDataApi.metadata',
    'MetaDataApi.dataproviders',
    'MetaDataApi.app'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'graphql_jwt.middleware.JSONWebTokenMiddleware',
    'admin_reorder.middleware.ModelAdminReorder',
]

ROOT_URLCONF = 'MetaDataApi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'MetaDataApi', 'templates')],
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

WSGI_APPLICATION = 'MetaDataApi.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'djongo',
#         'NAME': 'meta-data-api',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'meta-data-api',
        'USER': 'django',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

GRAPHENE = {
    'SCHEMA': 'MetaDataApi.schema.schema',
    'MIDDLEWARE': (
        'graphql_jwt.middleware.JSONWebTokenMiddleware',
        'graphene_django.debug.DjangoDebugMiddleware',
    )
}

settings_dir = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.dirname(settings_dir))
ML_models_dir = os.path.join(
    PROJECT_ROOT, "MetaDataApi/services/sound_classification/models")

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.' +
                'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.' +
                'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.' +
                'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.' +
                'NumericPasswordValidator',
    },
]

LOGIN_REDIRECT_URL = '/'

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = posixpath.join(*(BASE_DIR.split(os.path.sep) + ['static']))

ENV_PATH = os.path.abspath(os.path.dirname(__file__))
MEDIA_ROOT = os.path.join(ENV_PATH, 'media/')

MEDIA_URL = '/media/'

# Activate Django-Heroku.
django_heroku.settings(locals())

try:
    with open('api_keys.json') as f:
        api_keys = json.load(f)
except Exception as e:
    api_keys = {}

OAUTH_REDIRECT_URI = "https://meta-data-api.herokuapp.com/oauth2redirect/"
# OAUTH_REDIRECT_URI = "http://localhost:8000/oauth2redirect/"

# AWS
AWS_STORAGE_BUCKET_NAME = os.environ.get(
    'AWS_STORAGE_BUCKET_NAME') or api_keys.get("AWS_STORAGE_BUCKET_NAME")

AWS_S3_REGION_NAME = 'eu-central-1'  # e.g. us-east-2

AWS_ACCESS_KEY_ID = os.environ.get(
    'AWS_ACCESS_KEY_ID') or api_keys.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get(
    'AWS_SECRET_ACCESS_KEY') or api_keys.get("AWS_SECRET_ACCESS_KEY")

# avoid warning about public bucket
AWS_DEFAULT_ACL = 'public-read'

# Tell django-storages the domain to use to refer to static files.
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

# Tell the staticfiles app to use S3Boto3 storage when writing the collected
#  static files (when
# you run `collectstatic`).
STATICFILES_LOCATION = 'static'
STATICFILES_STORAGE = 'MetaDataApi.metadata.custom_storages.StaticStorage'

MEDIAFILES_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'MetaDataApi.metadata.custom_storages.MediaStorage'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': './debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

ADMIN_REORDER = (
    {'app': 'users', 'label': 'users',
     "models": (
         "auth.User",
         "users.Profile",
         "users.ThirdPartyProfile",
         "auth.Group"
     )
     },
    {'app': 'metadata', 'label': 'meta',
     'models': (
         'metadata.Schema',
         'metadata.Object',
         'metadata.ObjectRelation',
         'metadata.Attribute',
     )
     },
    {'app': 'metadata', 'label': 'instances',
     'models': (
         'metadata.ObjectInstance',
         'metadata.ObjectRelationInstance',
         'metadata.StringAttributeInstance',
         'metadata.DateTimeAttributeInstance',
         'metadata.IntAttributeInstance',
         'metadata.BoolAttributeInstance',
         'metadata.FloatAttributeInstance',
         'metadata.ImageAttributeInstance',
         'metadata.FileAttributeInstance',
     )
     },
    {'app': 'dataproviders', 'label': 'dataproviders'},
)
