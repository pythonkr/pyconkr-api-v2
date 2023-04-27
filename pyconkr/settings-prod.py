import os

from pyconkr.settings import *

DEBUG = False

ALLOWED_HOSTS += [
    "api.pycon.kr",
]

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
del MEDIA_ROOT

DEFAULT_FILE_STORAGE = "pyconkr.storage.MediaStorage"
STATICFILES_STORAGE = "pyconkr.storage.StaticStorage"

AWS_S3_ACCESS_KEY_ID = os.getenv("AWS_S3_ACCESS_KEY_ID")
AWS_S3_SECRET_ACCESS_KEY = os.getenv("AWS_S3_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION = "ap-northeast-2"
AWS_STORAGE_BUCKET_NAME = "pyconkr-api-v2-static"

REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = ("rest_framework.renderers.JSONRenderer",)
