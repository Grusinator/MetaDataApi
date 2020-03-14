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

# Copy project
COPY . /code/

RUN pipenv install --system --deploy --ignore-pipfile && pip install graphene-django

COPY init.sh /usr/local/bin/
RUN chmod u+x /usr/local/bin/init.sh

ENTRYPOINT [ "init.sh" ]





