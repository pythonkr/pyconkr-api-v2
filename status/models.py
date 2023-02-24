from django.db import models


class Status(models.Model):
    name = models.CharField(max_length=100)
    open_at = models.DateTimeField()
    close_at = models.DateTimeField()
