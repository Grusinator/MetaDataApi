"""
Django settings for MetaDataApi project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import sys
from enum import Enum

import django_heroku

from .env import Env

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
try:
    SECRET_KEY = os.environ['SECRET_KEY']
except:
    SECRET_KEY = 'ymcvw8ej))e=9jo89315q_r$imri(u0-ae!utev&ck4rs6cz+d'

TESTING = sys.argv[1:2] == ['test']
ENV = Env[os.environ.get('ENV', default=Env.LOCAL.value)]
DOCKER = bool(os.environ.get('DOCKER', default=False))
DEBUG = bool(os.environ.get('DEBUG', False))

def is_debugging():
    # gettrace() is none when not debugging
    return (sys.gettrace() is not None)

DEBUG = DEBUG or (ENV != Env.PROD) or is_debugging()

ALLOWED_HOSTS = []

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
    # 'corsheaders',
    # 'storages',
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

INSTALLED_APPS += (
    'users',
    'app',
    'metadata',
    'dataproviders',
    'dynamic_models',
)

MIDDLEWARE = [
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

DEFAULT_DATABASE = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'meta_data_api',
        'USER': 'django',
        'PASSWORD': 'dev1234',
        'HOST': 'db' if DOCKER else 'localhost',
        'PORT': '5432',
    }
}

DATABASES = CIRCLECI_TEST_DATABASE if ENV == Env.TEST else DEFAULT_DATABASE

print(f"starting env with settings DOCKER: {DOCKER}, ENV: {ENV.name}, DEBUG: {DEBUG}")

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators
dj_pass_val = 'django.contrib.auth.password_validation.'
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': f'{dj_pass_val}UserAttributeSimilarityValidator', },
    {'NAME': f'{dj_pass_val}MinimumLengthValidator', },
    {'NAME': f'{dj_pass_val}CommonPasswordValidator', },
    {'NAME': f'{dj_pass_val}NumericPasswordValidator', },
]

SILENCED_SYSTEM_CHECKS = ["fields.E303"] #, "fields.E002"]

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
# STATIC_ROOT = os.path.join(ENV_PATH, "app/static/")
# MEDIA_ROOT = os.path.join(ENV_PATH, "media/")

from .settings_specific.admin_reorder_settings import ADMIN_REORDER
from .settings_specific.aws_settings import *
from .settings_specific.celery_settings import *

OAUTH_REDIRECT_URI = ENV.get_url() + "oauth2redirect"

TEST_SETTINGS_EXCLUDE = ("rdf",)

# Activate Django-Heroku.
if (ENV != Env.TEST) and not TESTING:
    django_heroku.settings(locals())
