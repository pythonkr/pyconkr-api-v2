from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage, S3StaticStorage


class MediaStorage(S3Boto3Storage):
    def _get_security_token(self):
        return None


class StaticStorage(S3StaticStorage):
    def _get_security_token(self):
        return None
