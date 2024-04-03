from django.db import models
import uuid

from authentication.models import AppUser
from task.models import Task 

# Create your models here.
class TaskStep(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False) 
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task_steps', null=True, blank=True)
    name = models.TextField()
    description = models.TextField()
    status = models.CharField(max_length=16, default='NOT_STARTED', choices=[
            ('NOT_STARTED', 'NOT_STARTED'),
            ('ON_PROGRESS', 'ON_PROGRESS'),
            ('DONE', 'DONE'),
        ])
    step_order = models.IntegerField()
    user = models.ForeignKey(AppUser, on_delete = models.CASCADE)
