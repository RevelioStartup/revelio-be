from django.db import models

# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    budget = models.DecimalField(max_digits=20, decimal_places=2)
    objective = models.TextField()
    attendees = models.IntegerField()    
    theme = models.TextField()
    services = models.TextField()
    
    def __str__(self):
        return self.name