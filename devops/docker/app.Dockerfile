# Dockerfile

# Pull base image
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DOCKER 1

# Set work directory
WORKDIR /code/

# copy only neccecesary files for install
# if full repo is copied this step cannot be cached because code change all the time, 
# which makes install run again. 
COPY requirements.txt requirements.txt
COPY requirements requirements
COPY lib lib


RUN pip install -r requirements/prod.requirements.txt

# Copy full project
COPY . .


# set default cmd for running container
#CMD inv app.run
CMD cd /code/ && pwd && ls
#CMD python3 manage.py migrate --noinput && python3 manage.py runserver 0.0.0.0:80





