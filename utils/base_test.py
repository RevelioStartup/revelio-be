from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from authentication.models import AppUser
from subscription.models import Subscription
from package.models import Package

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

        cls.free_user = AppUser.objects.create_user(email='free@example.com', username='freeuser', password='test')
        cls.premium_user = AppUser.objects.create_user(email='premium@example.com', username='premiumuser', password='test')
        cls.another_user = AppUser.objects.create_user(email = 'anonymous@gmail.com', username='anonymous', password='test')
        
        Subscription.objects.create(user=cls.free_user, plan=free_package, end_date=timezone.now() + timedelta(days=365))
        Subscription.objects.create(user=cls.premium_user, plan=premium_package, end_date=timezone.now() + timedelta(days=30))