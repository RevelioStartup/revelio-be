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
        cls.free_package = cls.create_package(   name='Free',
            price=0,
            duration=0,
            event_planner=True,
            event_tracker=True,
            event_timeline=True,
            event_rundown=True,
            ai_assistant=False)
        
        cls.premium_package = cls.create_package(
            name='Premium',
            price=10000,
            duration=30,
            event_planner=True,
            event_tracker=True,
            event_timeline=True,
            event_rundown=True,
            ai_assistant=True
        )

        cls.free_user = cls.create_user('free@example.com', 'freeuser')
        cls.premium_user = cls.create_user('premium@example.com', 'premiumuser')
        cls.another_user = cls.create_user('anonymous@gmail.com', 'anonymous')

        Subscription.objects.create(user=cls.free_user, plan=cls.free_package, start_date=timezone.now(), end_date=timezone.now() + timedelta(days=365))
        Subscription.objects.create(user=cls.premium_user, plan=cls.premium_package, start_date=timezone.now(), end_date=timezone.now() + timedelta(days=30))

    @staticmethod
    def create_package(**features):
        return Package.objects.create(
            **features
        )

    @staticmethod
    def create_user(email, username):
        password = BaseUserManager().make_random_password()
        return AppUser.objects.create_user(email=email, username=username, password=password)
