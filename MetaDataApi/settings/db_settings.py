import os

from MetaDataApi.env import Env

ENV = Env[os.getenv('ENV', Env.LOCAL.value)]
DOCKER = bool(os.getenv('DOCKER', False))
DEBUG = bool(os.getenv('DEBUG', False))

USE_MONGO = True

CIRCLECI_TEST_DATABASE = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'circle_test',
        'USER': 'root',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# DEFAULT_DATABASE = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'meta_data_api',
#         'USER': 'django',
#         'PASSWORD': 'dev1234',
#         'HOST': 'db' if DOCKER else 'localhost',
#         'PORT': '5432',
#         'TEST': {
#             'NAME': 'meta_data_api_test',
#         },
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'meta_data_api',
        'CLIENT': {
            'host': 'host-name or ip address',
            'port': 27017,
            'username': 'django',
            'password': 'dev1234',
            'authSource': 'admin',
            'authMechanism': 'SCRAM-SHA-1'
        }
    }
}

# DATABASES = CIRCLECI_TEST_DATABASE if ENV == Env.TEST else DEFAULT_DATABASE
