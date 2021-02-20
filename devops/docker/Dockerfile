# Dockerfile

# Pull base image
FROM python:3.7

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DOCKER 1

# Set work directory
WORKDIR /code/

# Install dependencies
RUN pip install pipenv

# copy only neccecesary files for install
# if full repo is copied this step cannot be cached because code change all the time, 
# which makes install run again. 
COPY ../../Pipfile.lock Pipfile /code/
COPY ../../lib /code/lib


RUN pipenv install --system --deploy --ignore-pipfile && pip install graphene-django

# Copy full project
COPY ../.. /code/

# make init file executable
# RUN dos2unix /code/init.sh && apt-get --purge remove -y dos2unix && rm -rf /var/lib/apt/lists/*
RUN chmod +x /code/init.sh

# set default cmd for running container
CMD /code/init.sh
# CMD python3 /code/manage.py migrate --noinput && python3 /code/manage.py runserver 0.0.0.0:80





