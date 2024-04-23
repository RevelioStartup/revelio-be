from datetime import timedelta
from django.utils import timezone
from django.test import TestCase
from rest_framework.test import APIClient

from authentication.models import AppUser
from subscription.models import Subscription
from django.urls import reverse


# Create your tests here.
class SubscriptionHistoryTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = AppUser.objects.create_user(email='user@example.com', username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        
        self.subscription = Subscription.objects.create(user=self.user, plan='PREMIUM', end_date=timezone.now() + timedelta(days=30))
        self.url = reverse('history') 
        
    def test_get_subscription_history(self):
        response = self.client.get(self.url)
        
        print(response)