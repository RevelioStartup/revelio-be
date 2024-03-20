from django.db import models
from event.models import Event

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    status = models.CharField(max_length=16, default='NONE', choices=[
            ('Not Started', 'Not Started'),
            ('On Progress', 'On Progress'),
            ('Done', 'Done'),
        ])
    event = models.ForeignKey(Event, related_name='tasks', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title