from MetaDataApi.utils.api_keys import get_setting_from_env_var_or_json_file

AWS_STORAGE_BUCKET_NAME = get_setting_from_env_var_or_json_file("AWS_STORAGE_BUCKET_NAME")

AWS_S3_REGION_NAME = 'eu-central-1'  # e.g. us-east-2

AWS_ACCESS_KEY_ID = get_setting_from_env_var_or_json_file("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = get_setting_from_env_var_or_json_file("AWS_SECRET_ACCESS_KEY")

# avoid warning about public bucket
AWS_DEFAULT_ACL = 'public-read'

# Tell django-storages the domain to use to refer to static files.
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

# Tell the staticfiles app to use S3Boto3 storage when writing the collected
#  static files (when
# you run `collectstatic`).
STATICFILES_LOCATION = 'static'
STATICFILES_STORAGE = 'MetaDataApi.custom_storages.StaticStorage'

PUBLIC_MEDIA_LOCATION = 'media/public'
PUBLIC_FILE_STORAGE = 'MetaDataApi.custom_storages.PublicMediaStorage'

PRIVATE_MEDIA_LOCATION = 'media/private'
PRIVATE_FILE_STORAGE = 'MetaDataApi.custom_storages.PrivateMediaStorage'
