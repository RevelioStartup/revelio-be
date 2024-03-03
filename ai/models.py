from django.db import models
from django.utils import timezone
from datetime import date
import uuid

from authentication.models import AppUser 

# Create your models here.
class RecommendationHistory(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False) 
    user = models.ForeignKey(AppUser, on_delete = models.CASCADE)
    date = models.DateField(default = date.today)
    prompt = models.TextField()
    output = models.TextField()