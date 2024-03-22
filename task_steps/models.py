from django.db import models
from datetime import date
import uuid

from authentication.models import AppUser
from task.models import Task 

# Create your models here.
class TaskStep(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False) 
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task_steps')
    name = models.TextField()
    output = models.TextField()
    description = models.TextField()
    status = models.CharField(max_length=16, default='NONE', choices=[
            ('NOT_STARTED', 'NOT_STARTED'),
            ('ON_PROGRESS', 'ON_PROGRESS'),
            ('DONE', 'DONE'),
        ])
    step_order = models.IntegerField()