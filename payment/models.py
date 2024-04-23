import uuid
from django.db import models
from authentication.models import AppUser
# Create your models here.

class Transaction(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False) 
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='transactions')
    midtrans_id = models.CharField(max_length=1024, unique=True, db_index=True)
    order_id = models.CharField(max_length=1024, unique=True, db_index=True)

    price = models.BigIntegerField()
    checkout_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()

    payment_method = models.CharField(max_length=30, blank=True, null=True)
    payment_channel = models.CharField(max_length=30, blank=True, null=True)
    payment_type = models.CharField(max_length=30, blank=True, null=True)
    payment_destination = models.CharField(max_length=1024, blank=True, null=True)

    transaction_details = models.TextField(blank=True, null=True)  # JSON response
    paid_at_date = models.DateTimeField(blank=True, null=True)

    status = models.CharField(max_length=16, default='PENDING', choices=[
        ('PENDING', 'Pending'),
        ('CANCELLED', 'Cancelled'),
        ('PROCESSING', 'Processing'),
        ('SUCCESS', 'Success'),
        ('REFUND', 'Refund'),
        ('EXPIRED', 'Expired'),
    ], db_index=True)

    class Meta:
        ordering = ['-checkout_date']

    def __str__(self):
        return f"{self.order_id} - {self.status}"