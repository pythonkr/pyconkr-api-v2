import os

DEBUG = False

# RDS
DATABASES = {
    "default": {
        "ENGINE": "mysql.connector.django",
        "NAME": os.getenv("AWS_RDS_DATABASE"),
        "USER": os.getenv("AWS_RDS_USER_ID"),
        "PASSWORD": os.getenv("AWS_RDS_PW"),
        "HOST": os.getenv("AWS_RDS_HOST"),
        "PORT": os.getenv("AWS_RDS_PORT"),
    }
}

# django-storages: S3
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
STATICFILES_STORAGE = "storages.backends.s3boto3.S3StaticStorage"
AWS_S3_ACCESS_KEY_ID = os.getenv("AWS_S3_ACCESS_KEY_ID")
AWS_S3_SECRET_ACCESS_KEY = os.getenv("AWS_S3_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = "pyconkr-api-v2-static"
