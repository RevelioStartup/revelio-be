from django.db import models

class Package(models.Model):
    name = models.TextField()
    price = models.IntegerField()
    duration = models.IntegerField()
    event_planner = models.BooleanField(default=False)
    event_tracker = models.BooleanField(default=False)
    event_timeline = models.BooleanField(default=False)
    event_rundown = models.BooleanField(default=False)
    ai_assistant = models.BooleanField(default=False)
