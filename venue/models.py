from django.db import models

# Create your models here.

from django.core.files.storage import default_storage

class Venue(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    price = models.IntegerField()
    status = models.CharField(max_length=16, default='NONE', choices=[
            ('NONE', 'NONE'),
            ('PENDING', 'PENDING'),
            ('WAITLIST', 'WAITLIST'),
            ('CONFIRMED', 'CONFIRMED'),
            ('CANCELLED', 'CANCELLED'),
        ])
    contact_name = models.CharField(max_length=255)
    contact_phone_number = models.CharField(max_length=15)
    event = models.IntegerField()

    def __str__(self):
        return self.name

class Photo(models.Model):
    venue = models.ForeignKey(Venue, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(storage = default_storage, upload_to='photos/')

    def __str__(self):
        return self.image.url