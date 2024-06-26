import os

#settings
AWS_S3_REGION_NAME = 'sfo3'
AWS_S3_ENDPOINT_URL = "https://sfo3.digitaloceanspaces.com"
AWS_ACCESS_KEY_ID=os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY=os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME=os.environ.get("AWS_STORAGE_BUCKET_NAME", "plannit-spaces")
AWS_S3_OBJECT_PARAMETERS = { 'CacheControl': 'max-age=86400', }
AWS_DEFAULT_ACL = 'public-read'
AWS_BUCKET_ACL = 'public-read'
AWS_IS_GZIPPED = True
AWS_S3_USE_SSL = True
AWS_QUERYSTRING_AUTH = False

# static settings
AWS_LOCATION= f'https://{AWS_STORAGE_BUCKET_NAME}.{AWS_S3_REGION_NAME}.digitaloceanspaces.com'
STATICFILES_STORAGE ="dmp.cdn.backends.StaticRootS3Boto3Storage"
# STATIC_URL = f'https://{AWS_LOCATION}/static/'

# media settings
# PUBLIC_MEDIA_LOCATION = 'media'
# MEDIA_URL = f'https://{STATIC_URL}/{PUBLIC_MEDIA_LOCATION}/'
DEFAULT_FILE_STORAGE ="dmp.cdn.backends.MediaRootS3Boto3Storage"

