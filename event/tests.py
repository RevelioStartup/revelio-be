from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from authentication.models import AppUser

# Create your tests here.
EVENT_LINK = reverse('event:event_view')

class EventTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = AppUser.objects.create_user(email='email@email.com',username='testuser',password='test')
        self.client.force_authenticate(user=self.user)
        
    def test_get_event(self):
        response = self.client.get(EVENT_LINK)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "Event")