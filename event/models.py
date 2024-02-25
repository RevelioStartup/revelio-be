from django.db import models
import uuid

from authentication.models import AppUser 

# Create your models here.
class Event(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False) 
    user = models.ForeignKey(AppUser, on_delete = models.CASCADE)
    name = models.CharField(max_length=255)
    date = models.DateField()
    budget = models.DecimalField(max_digits=20, decimal_places=2)
    objective = models.TextField()
    attendees = models.IntegerField()    
    theme = models.TextField()
    services = models.TextField()
    
    def __str__(self):
        return self.name