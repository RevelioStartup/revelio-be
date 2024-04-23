from django.db import models
from django.utils import timezone

from authentication.models import AppUser

# Create your models here.
class Subscription(models.Model):
    OPTION_PLANS = (
        ('FREE', 'Free'),
        ('PREMIUM', 'Premium'),
    )
    
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    plan = models.CharField(choices=OPTION_PLANS, max_length=10)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

    @property
    def is_active(self):
        return self.end_date > timezone.now()