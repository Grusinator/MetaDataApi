import os

from dotenv import load_dotenv

load_dotenv()

USE_AWS = True

if USE_AWS:
    AWS_S3_REGION_NAME = 'eu-central-1'  # e.g. us-east-2
    AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

    # avoid warning about public bucket
    AWS_DEFAULT_ACL = 'public-read'

    # Tell django-storages the domain to use to refer to static files.
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

    # Tell the staticfiles app to use S3Boto3 storage when writing the collected
    #  static files (when
    # you run `collectstatic`).
    STATICFILES_LOCATION = 'static'
    STATICFILES_STORAGE = 'MetaDataApi.custom_storages.StaticStorage'

    PUBLIC_MEDIA_LOCATION = 'media/public'
    PUBLIC_FILE_STORAGE = 'MetaDataApi.custom_storages.PublicMediaStorage'

    PRIVATE_MEDIA_LOCATION = 'media/private'
    PRIVATE_FILE_STORAGE = 'MetaDataApi.custom_storages.PrivateMediaStorage'

    # separation of file types, currently only one for data dump / upload.
    DATAFILE_STORAGE_PATH = "datafiles/"
