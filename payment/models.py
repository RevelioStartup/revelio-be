import uuid
from django.db import models
from authentication.models import AppUser
from package.models import Package

class Transaction(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False) 
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='transactions')

    midtrans_url = models.URLField(unique=True, null=True, blank=True)
    midtrans_transaction_id = models.CharField(max_length=1024, unique=True, db_index=True, null=True, default=None)
    order_id = models.UUIDField(unique=True, db_index=True)

    price = models.BigIntegerField()
    checkout_time = models.DateTimeField(auto_now_add=True)
    expiry_time = models.DateTimeField(null=True, blank=True)

    payment_type = models.CharField(max_length=30, blank=True, null=True)
    payment_merchant = models.CharField(max_length=1024, blank=True, null=True)

    status = models.CharField(max_length=30, blank=True, null=True)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='transactions')

    class Meta:
        ordering = ['-checkout_time']

    def __str__(self):
        return f"{self.order_id} - {self.status}"

