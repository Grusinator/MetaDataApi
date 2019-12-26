# CELERY
# CELERY_BROKER_URL = 'pyamqp://django:dev1234@localhost:5672/meta_data_api'
#: Only add pickle to this list if your broker is secured
#: from unwanted access (see userguide/security.html)
from MetaDataApi.settings import DOCKER

CELERY_RESULT_BACKEND = 'django-db'
CELERY_TASK_SERIALIZER = 'json'
CELERY_CACHE_BACKEND = 'django-cache'

CELERY_BROKER_URL = 'redis://redis:6379' if DOCKER else 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'

CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_SEND_SENT_EVENT = True
CELERY_SEND_EVENTS = True
