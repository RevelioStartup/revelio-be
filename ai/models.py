from django.db import models
import uuid

from authentication.models import AppUser 

# Create your models here.
class AIRecommendation(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False) 
    user = models.ForeignKey(AppUser, on_delete = models.CASCADE)
    date = models.DateField()
    prompt = models.TextField()
    output = models.TextField()