#!/bin/sh
python3 /code/manage.py migrate --noinput && python3 /code/manage.py runserver 0.0.0.0:80