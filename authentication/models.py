from django.db import models
from django.contrib.auth.models import AbstractUser

class AppUser(AbstractUser):
    is_verified_user = models.BooleanField(default=False)