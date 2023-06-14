from django.db import models
from django.contrib.auth.models import User


class UserExt(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_img = models.ImageField(null=True, blank=True)
    bio = models.TextField()
