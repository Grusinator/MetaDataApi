from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


# AWS custom storages
class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION


class PublicMediaStorage(S3Boto3Storage):
    location = settings.PUBLIC_MEDIA_LOCATION
    file_overwrite = True


class MediaStorage(PublicMediaStorage):
    pass


class PrivateMediaStorage(S3Boto3Storage):
    location = settings.PRIVATE_MEDIA_LOCATION
    default_acl = 'private'
    file_overwrite = True
    custom_domain = False
