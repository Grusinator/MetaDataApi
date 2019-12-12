# Create your tasks here
from __future__ import absolute_import, unicode_literals

import celery


@celery.shared_task
def add(x, y):
    return x + y


@celery.shared_task
def mul(x, y):
    return x * y


@celery.shared_task
def xsum(numbers):
    return sum(numbers)
