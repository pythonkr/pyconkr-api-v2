import os

import pymysql

from pyconkr.settings import *

pymysql.install_as_MySQLdb()

DEBUG = False

ALLOWED_HOSTS += [
    "api.pycon.kr",
]

# RDS
if os.environ.get("AWS_PSQL_HOST"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "HOST": os.getenv("AWS_PSQL_HOST"),
            "PORT": os.getenv("AWS_PSQL_PORT"),
            "NAME": os.getenv("AWS_PSQL_DATABASE"),
            "USER": os.getenv("AWS_PSQL_USER_ID"),
            "PASSWORD": os.getenv("AWS_PSQL_PW"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
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
