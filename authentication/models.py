from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.files.storage import default_storage

class AppUser(AbstractUser):
    is_verified_user = models.BooleanField(default=False)
    real_username = models.TextField(null=True)
    real_email = models.EmailField(null=True)
    
    def __str__(self):
        return super().username

class Profile(models.Model):
    user = models.OneToOneField(AppUser, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(storage = default_storage, upload_to='profile_pictures/', blank=True)

class UserToken(models.Model):
    user = models.OneToOneField(AppUser, on_delete=models.CASCADE)
    token = models.TextField(unique = True)
    shortened_token = models.TextField(unique=True)