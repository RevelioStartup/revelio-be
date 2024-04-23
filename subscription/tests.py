from django.test import TestCase
from rest_framework.test import APIClient

from authentication.models import AppUser


# Create your tests here.
class SubscriptionHistoryTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = AppUser.objects.create_user(email='user@example.com', username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        
        