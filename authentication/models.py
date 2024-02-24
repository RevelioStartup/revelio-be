from django.db import models
from django.contrib.auth.models import AbstractUser

class AppUser(AbstractUser):
    is_verified_user = models.BooleanField(default=False)

class Profile(models.Model):
    user = models.OneToOneField(AppUser, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
