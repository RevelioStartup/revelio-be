from django.db import models
import uuid
from task_steps.models import TaskStep
from datetime import datetime

class Timeline(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    start_datetime = models.DateTimeField(default=datetime.now)
    end_datetime = models.DateTimeField(default=datetime.now)
    task_step = models.ForeignKey(TaskStep, on_delete=models.CASCADE, related_name='timelines')

