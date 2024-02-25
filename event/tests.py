from datetime import date
from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from authentication.models import AppUser
from event.models import Event
from event.serializers import EventSerializer

# Create your tests here.
EVENT_LIST_LINK = reverse('event:list')

class EventTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = AppUser.objects.create_user(email='email@email.com',username='testuser',password='test')
        self.client.force_authenticate(user=self.user)
        
        self.event_attributes = {
            "user": self.user,
            "name": "Revelio Onboarding",
            "date": date.today(),
            "budget": Decimal('20000000'),
            "objective": "To onboard new employees",
            "attendees": 100,
            "theme": "Harry Potter",
            "services": "Catering, Decorations, Music"
        }
        self.model = Event.objects.create(**self.event_attributes)
        self.serializer = EventSerializer(instance = self.model)
        
        self.EVENT_DETAIL_LINK = reverse('event:detail', kwargs={'id': self.model.id})
    
    def test_get_list_event(self):
        try:
            response = self.client.get(EVENT_LIST_LINK)
        except NotImplementedError as e:
            self.assertEqual(str(e), "This method is not implemented yet!")
        
    def test_get_detail_event(self):
        try:
            response = self.client.get(self.EVENT_DETAIL_LINK)
            data = self.serializer.data
            self.assertEqual(response.status_code, 200)
            self.assertEqual(set(data.keys()), set(response.data))
        except NotImplementedError as e:
            self.assertEqual(str(e), "This method is not implemented yet!")