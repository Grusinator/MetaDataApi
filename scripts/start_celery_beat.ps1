pipenv run celery -A MetaDataApi beat --l info --scheduler django_celery_beat.schedulers:DatabaseScheduler -P eventlet
