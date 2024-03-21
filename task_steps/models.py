from django.db import models
from datetime import date
import uuid

from authentication.models import AppUser 

# Create your models here.
class TaskStep(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False) 
    # foreign key ke task
    name = models.TextField()
    output = models.TextField()
    description = models.TextField()
    status = models.CharField(max_length=16, default='NONE', choices=[
            ('NOT_STARTED', 'NOT_STARTED'),
            ('ON_PROGRESS', 'ON_PROGRESS'),
            ('DONE', 'DONE'),
           
        ])
    step_order = models.IntegerField()