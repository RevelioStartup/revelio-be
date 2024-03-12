from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.storage import default_storage

class AppUser(AbstractUser):
    is_verified_user = models.BooleanField(default=False)

class Profile(models.Model):
    user = models.OneToOneField(AppUser, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(storage = default_storage, upload_to='profile_pictures/', blank=True)
