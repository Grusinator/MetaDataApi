from __future__ import absolute_import, unicode_literals

import os

# TODO this django.setup() might not be nice, acording to:
#  https://stackoverflow.com/questions/39676684/django-apps-arent-loaded-yet-celery-tasks
import celery
# from dataproviders.tasks import fetch_data_for_each_user
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
# django.setup()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MetaDataApi.settings')

app = celery.Celery('meta_data_api')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'fetch_data_for_each_user_every_midnight': {
        'task': 'dataproviders.tasks.fetch_data_for_each_user',
        'schedule': crontab(minute=0, hour=0)  # every day midnight
    }
}
