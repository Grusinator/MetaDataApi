from __future__ import absolute_import, unicode_literals

import os

# TODO this django.setup() might not be nice, acording to:
#  https://stackoverflow.com/questions/39676684/django-apps-arent-loaded-yet-celery-tasks
from celery import Celery
# set the default Django settings module for the 'celery' program.
from celery.schedules import crontab

# django.setup()

# from dataproviders.tasks import fetch_all_data_from_providers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MetaDataApi.settings')

app = Celery('meta_data_api')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

    midnight = crontab(minute=0, hour=0)
    every_minute = crontab()
    # sender.add_periodic_task(every_minute, fetch_all_data_from_providers, name='start fetching data from providers')


@app.task
def test(arg):
    print(arg)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'dataproviders.tasks.fetch_all_data_from_providers',
        'schedule': 30.0,
    },
}
