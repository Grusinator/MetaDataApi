# CELERY
CELERY_BROKER_URL = 'pyamqp://django:dev1234@localhost:5672/meta_data_api'
#: Only add pickle to this list if your broker is secured
#: from unwanted access (see userguide/security.html)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_BACKEND = 'django-db'
CELERY_TASK_SERIALIZER = 'json'
CELERY_CACHE_BACKEND = 'django-cache'
