"""
Django settings for MetaDataApi project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import sys

from MetaDataApi.env import Env
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from MetaDataApi.load_env import load_env

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
load_env(BASE_DIR)
SECRET_KEY = os.environ.get('SECRET_KEY', 'ymcvw8ej))e=9jo89315q_r$imri(u0-ae!utev&ck4rs6cz+d')
TESTING = sys.argv[1:2] == ['test']
ENV = Env[os.environ.get('ENV', default=Env.LOCAL.value)]
DOCKER = bool(os.environ.get('DOCKER', default=False))
DEBUG = bool(os.environ.get('DEBUG', False))


def is_debugging():
    # gettrace() is none when not debugging
    return (sys.gettrace() is not None)


DEBUG = DEBUG or (ENV not in (Env.PROD, Env.PREPROD)) or is_debugging()
DEBUG_PROPAGATE_EXCEPTIONS = (not DEBUG) and (ENV == ENV.PROD)

ALLOWED_HOSTS = ["metadataapi.grusinator.com", "metadataapi.wsh-home.dk"]

if ENV != Env.PROD:
    ALLOWED_HOSTS += ("localhost", "127.0.0.1", "0.0.0.0")

CORS_ORIGIN_WHITELIST = [
    'http://localhost:8000',
    'https://localhost:8000',
    'http://127.0.0.1:8000',
    'https://127.0.0.1:8000',
]

CORS_ALLOW_CREDENTIALS = True
# CORS_ORIGIN_ALLOW_ALL = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'graphene_django',
    # 'rest_framework',
    # 'oauth2_provider',
    'corsheaders',
    'storages',
    'admin_reorder',
    # 'graphene_file_upload',
    'django_celery_results',
    'django_celery_beat',
    'djcelery_model',
    # 'social_django',
]

# apps to run json2model
INSTALLED_APPS += (
    'mutant',
    'mutant.contrib.text',
    'mutant.contrib.boolean',
    'mutant.contrib.temporal',
    'mutant.contrib.file',
    'mutant.contrib.numeric',
    'mutant.contrib.related',
    # # 'mutant.contrib.web',
    'json2model'
)
# Error
# object: activity, could not be created due to error: duplicate key value violates unique constraint "django_content_type_app_label_model_76bd3d3b_uniq"
# DETAIL:  Key (app_label, model)=(dynamic_models, activity) already exists.
# APP_LABEL_DYNAMIC_MODELS = "dynamic_models"
RELATE_TO_USER = True

INSTALLED_APPS += (
    'users',
    'app',
    'metadata',
    'dataproviders',
    'dynamic_models',
)

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'admin_reorder.middleware.ModelAdminReorder',
]

ROOT_URLCONF = 'MetaDataApi.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'MetaDataApi.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases


CIRCLECI_TEST_DATABASE = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'circle_test',
        'USER': 'root',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

APPEND_SLASH = True

DEFAULT_DATABASE = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'meta_data_api',
        'USER': 'django',
        'PASSWORD': 'dev1234',
        'HOST': 'db' if DOCKER else 'localhost',
        'PORT': '5432',
        'TEST': {
            'NAME': 'meta_data_api_test',
        },
    }
}

AUTHENTICATION_BACKENDS = [
    'graphql_jwt.backends.JSONWebTokenBackend',
    'django.contrib.auth.backends.ModelBackend',
]

DATABASES = CIRCLECI_TEST_DATABASE if ENV == Env.TEST else DEFAULT_DATABASE

print(f"starting env with settings DOCKER: {DOCKER}, ENV: {ENV.name}, DEBUG: {DEBUG}, TESTING: {TESTING}")

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators
dj_pass_val = 'django.contrib.auth.password_validation.'
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': f'{dj_pass_val}UserAttributeSimilarityValidator', },
    {'NAME': f'{dj_pass_val}MinimumLengthValidator', },
    {'NAME': f'{dj_pass_val}CommonPasswordValidator', },
    {'NAME': f'{dj_pass_val}NumericPasswordValidator', },
]

SILENCED_SYSTEM_CHECKS = ["fields.E303"]  # , "fields.E002"]

GRAPHENE = {
    'SCHEMA': 'MetaDataApi.schema.schema',
    'MIDDLEWARE': (
        'graphql_jwt.middleware.JSONWebTokenMiddleware',
        'graphene_django.debug.DjangoDebugMiddleware',
    )
}

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
ENV_PATH = os.path.abspath(os.path.dirname(__file__))
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'app/../../app/static/'),
]
# STATIC_ROOT = os.path.join(ENV_PATH, "app/static/")
# MEDIA_ROOT = os.path.join(ENV_PATH, "media/")

from MetaDataApi.settings.admin_reorder_settings import ADMIN_REORDER
from MetaDataApi.settings.aws_settings import *
from MetaDataApi.settings.celery_settings import *
from MetaDataApi.settings.db_settings import *

OAUTH_REDIRECT_URI = ENV.get_url() + "oauth2redirect"

TEST_SETTINGS_EXCLUDE = ("rdf",)

# Activate Django-Heroku.
# if (ENV != Env.TEST) and not TESTING:
#     django_heroku.settings(locals())
