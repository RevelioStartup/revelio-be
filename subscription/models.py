from django.db import models
from django.utils import timezone

from authentication.models import AppUser
from package.models import Package

# Create your models here.
class Subscription(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    plan = models.ForeignKey(Package, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

    @property
    def is_active(self):
        return self.end_date > timezone.now() and self.plan.name != 'Free'