from django.db import models

# Create your models here.

from django.db import models

class Venue(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    price = models.IntegerField()
    status = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255)
    contact_phone_number = models.CharField(max_length=15)
    event = models.IntegerField()

    def __str__(self):
        return self.name

class Photo(models.Model):
    venue = models.ForeignKey(Venue, related_name='photos', on_delete=models.CASCADE)
    image = models.URLField()

    def __str__(self):
        return self.image
