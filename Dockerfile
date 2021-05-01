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
COPY requirements.txt /code/requirements.txt
COPY requirements /code/requirements
COPY lib /code/lib


RUN pip install -r requirements/prod.requirements.txt

# Copy full project
COPY . /code/


# set default cmd for running container
CMD inv app.run
# CMD python3 /code/manage.py migrate --noinput && python3 /code/manage.py runserver 0.0.0.0:80





