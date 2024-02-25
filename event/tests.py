from datetime import date
from decimal import Decimal
import uuid
from django.test import TestCase
from django.urls import NoReverseMatch, reverse
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
        response = self.client.get(EVENT_LIST_LINK)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)         
    
    def test_get_list_event_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(EVENT_LIST_LINK)
        self.assertEqual(response.status_code, 401)
        
    def test_get_detail_event(self):
        response = self.client.get(self.EVENT_DETAIL_LINK)
        data = self.serializer.data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(data.keys()), set(response.data))
    
    def test_get_detail_event_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.EVENT_DETAIL_LINK)
        self.assertEqual(response.status_code, 401)
        
    def test_get_invalid_detail_event(self):
        with self.assertRaises(NoReverseMatch):
            self.client.get(reverse('event:detail', kwargs={'id': 'invalid id'}))
                
    def test_get_not_found_event(self):
        new_uuid = uuid.uuid4()
        while new_uuid == self.model.id:
            new_uuid = uuid.uuid4()
        
        response = self.client.get(reverse('event:detail', kwargs={'id': new_uuid}))
        
        self.assertEqual(response.status_code, 404)
        
    def test_post_event(self):
        response = self.client.post(EVENT_LIST_LINK, self.event_attributes)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Event.objects.count(), 2)
        
    def test_post_invalid_event(self):
        response = self.client.post(EVENT_LIST_LINK, {})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Event.objects.count(), 1)
        
    def test_post_missing_event(self):
        response = self.client.post(EVENT_LIST_LINK, {
            "user": self.user,
            # "name": "Revelio Onboarding",
            "date": date.today(),
            "budget": Decimal('20000000'),
            "objective": "To onboard new employees",
            "attendees": 100,
            "theme": "Harry Potter",
            "services": "Catering, Decorations, Music"
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(response.data['name'], ['This field is required.'])
    
    def test_post_unauthenticated_event(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(EVENT_LIST_LINK, self.event_attributes)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(Event.objects.count(), 1)
        
    def test_delete_event(self):
        response = self.client.delete(self.EVENT_DETAIL_LINK)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Event.objects.count(), 0)
        
    def test_delete_unauthenticated_event(self):
        self.client.force_authenticate(user=None)
        response = self.client.delete(self.EVENT_DETAIL_LINK)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(Event.objects.count(), 1)