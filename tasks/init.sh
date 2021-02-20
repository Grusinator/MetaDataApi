#!/bin/bash

python3 /code/manage.py migrate --noinput && python3 /code/manage.py runserver 0.0.0.0:80
# gunicorn -b 0.0.0.0:8000 metadataapi.wsgi:application