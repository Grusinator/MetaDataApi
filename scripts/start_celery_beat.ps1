pipenv run celery -A MetaDataApi beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
