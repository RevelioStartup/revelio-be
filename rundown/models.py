from django.db import models
from event.models import Event
import uuid

class Rundown(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False) 
    start_time = models.TimeField()
    end_time = models.TimeField()
    description = models.TextField()
    rundown_order = models.IntegerField()
    event = models.ForeignKey(Event, related_name='rundown', on_delete=models.CASCADE)
