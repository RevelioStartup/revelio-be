from datetime import timedelta
from django.utils import timezone
from django.test import TestCase
from rest_framework.test import APIClient

from authentication.models import AppUser
from package.models import Package
from subscription.models import Subscription
from django.urls import reverse


# Create your tests here.
class SubscriptionHistoryTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = AppUser.objects.create_user(email='user@example.com', username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        
        self.package = Package.objects.create(name='PREMIUM', price=100, duration=30, event_planner=True, event_tracker=True, event_timeline=True, event_rundown=True, ai_assistant=True)
        
        self.subscription = Subscription.objects.create(user=self.user, plan=self.package, end_date=timezone.now() + timedelta(days=30))
        self.url = reverse('history') 
        
    def test_get_subscription_history(self):
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['plan'], 'PREMIUM')
    
    def test_get_subscription_history_no_subscription(self):
        Subscription.objects.all().delete()
        
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])
        
    def test_get_subscription_history_unauthenticated(self):
        self.client.logout()
        
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 401)
        
class LatestSubscriptionTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = AppUser.objects.create_user(email='user@example.com', username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        
        self.subscription = Subscription.objects.create(user=self.user, plan='PREMIUM', end_date=timezone.now() + timedelta(days=30))
        self.url = reverse('latest') 
        
    def test_get_latest_subscription(self):
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['plan'], 'PREMIUM')