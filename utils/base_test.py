from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from authentication.models import AppUser
from subscription.models import Subscription
from package.models import Package
from django.contrib.auth.models import BaseUserManager

class BaseTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        free_package = Package.objects.create(
            name='Free Package',
            price=0,
            duration=365,  
            event_planner=True,
            event_tracker=True,
            event_timeline=True,
            event_rundown=True,
            ai_assistant=False
        )

        premium_package = Package.objects.create(
            name='Premium Package',
            price=10000,
            duration=30,  
            event_planner=True,
            event_tracker=True,
            event_timeline=True,
            event_rundown=True,
            ai_assistant=True
        )

        free_password = BaseUserManager().make_random_password()
        premium_password = BaseUserManager().make_random_password()
        anonymous_password = BaseUserManager().make_random_password()

        cls.free_user = AppUser.objects.create_user(email='free@example.com', username='freeuser', password=free_password)
        cls.premium_user = AppUser.objects.create_user(email='premium@example.com', username='premiumuser', password=premium_password)
        cls.another_user = AppUser.objects.create_user(email='anonymous@gmail.com', username='anonymous', password=anonymous_password)

        
        Subscription.objects.create(user=cls.free_user, plan=free_package, end_date=timezone.now() + timedelta(days=365))
        Subscription.objects.create(user=cls.premium_user, plan=premium_package, end_date=timezone.now() + timedelta(days=30))