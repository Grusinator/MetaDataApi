# Dockerfile

# Pull base image
FROM python:3.7

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /MetaDataApi/

# Install dependencies
RUN pip install pipenv

# Copy project
COPY . /MetaDataApi/

RUN pipenv install --system --deploy --dev




