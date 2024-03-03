from django.db import models
from django.utils import timezone
import uuid

from authentication.models import AppUser 

# Create your models here.
class RecommendationHistory(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False) 
    user = models.ForeignKey(AppUser, on_delete = models.CASCADE)
    date = models.DateField(default = timezone.now)
    prompt = models.TextField()
    output = models.TextField()