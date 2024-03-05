from django.db import models

# Create your models here.

class Vendor(models.Model):
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

class PhotoVendor(models.Model):
    vendor = models.ForeignKey(Vendor, related_name='photos', on_delete=models.CASCADE)
    image = models.URLField()

    def __str__(self):
        return self.image
