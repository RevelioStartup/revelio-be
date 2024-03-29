from datetime import date
from rest_framework.test import APIClient
from django.test import TestCase
from django.urls import reverse
from ai.models import RecommendationHistory
from ai.serializers import RecommendationHistorySerializer
from authentication.models import AppUser
from event.models import Event
import json
from decimal import Decimal
from uuid import UUID

# Create your tests here.

ASSISTANT_LINK = reverse('ai:assistant')
AUTOFILL_LINK = reverse('ai:autofill')

class AssistantTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = AppUser.objects.create_user(email='email@email.com',username='testuser',password='test')
        self.another_user = AppUser.objects.create_user(email = 'anonymous@gmail.com', username='anonymous', password='test')
        
        self.client.force_authenticate(user=self.user)
        self.event_data = {
            "id": UUID("9fdfb487-5101-4824-8c3b-0775732aacda"),
            "user": self.user,
            "name": "Revelio Onboarding",
            "date": date.today(),
            "budget": Decimal('20000000'),
            "objective": "To onboard new employees",
            "attendees": 100,
            "theme": "Harry Potter",
            "services": "Catering, Decorations, Music"
        }
        self.event = Event.objects.create(**self.event_data)

    def test_assitant_valid(self):
        data = {
            'prompt' : 'Berikan rekomendasi tempat untuk acara ulang tahun di Braga, Bandung.',
            'type': 'specific',
            'event_id': str(self.event.id)
        }
        response = self.client.post(ASSISTANT_LINK, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
    
    def test_assitant_specific_no_event(self):
        data = {
            'prompt' : 'Berikan rekomendasi tempat untuk acara ulang tahun di Braga, Bandung.',
            'type': 'specific'
        }
        response = self.client.post(ASSISTANT_LINK, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_assitant_valid_general(self):
        data = {
            'prompt' : 'Di mana letak Braga dari ITB bandung?',
            'type': 'general',
            'event_id': str(self.event.id)
        }
        response = self.client.post(ASSISTANT_LINK, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_assistant_empty_input(self):
        data = {
            'prompt' : ', .',
            'event_id': str(self.event.id)
        }
        response = self.client.post(ASSISTANT_LINK, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['msg'], 'Make sure you are putting a correct prompt to the assistant.')

class HistoryTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = AppUser.objects.create_user(email='email@email.com',username='testuser',password='test')
        self.another_user = AppUser.objects.create_user(email = 'anonymous@gmail.com', username='anonymous', password='test')
        
        self.client.force_authenticate(user=self.user)
        self.event_data = {
            "id": UUID("9fdfb487-5101-4824-8c3b-0775732aacda"),
            "user": self.user,
            "name": "Revelio Onboarding",
            "date": date.today(),
            "budget": Decimal('20000000'),
            "objective": "To onboard new employees",
            "attendees": 100,
            "theme": "Harry Potter",
            "services": "Catering, Decorations, Music"
        }
        self.event = Event.objects.create(**self.event_data)
        self.recommendation_attributes = {
            "user": self.user,
            "event": self.event,
            "prompt": "Berikan rekomendasi tempat untuk acara ulang tahun di Braga, Bandung.",
            "output": "Berikut adalah 5 tempat makan favorit di Bandung.",
            "list": "[\"Tempat makan 1\", \"Tempat makan 2\", \"Tempat makan 3\"]",
            "keyword": "[\"Keyword 1\", \"Keyword 2\"]",
            "type": "specific"
        }
        self.model = RecommendationHistory.objects.create(**self.recommendation_attributes)
        self.serializer = RecommendationHistorySerializer(instance = self.model)
        self.HISTORY_LINK = reverse('ai:history', kwargs={'event_id': str(self.event.id)})

    def test_get_list_recommendation_history(self):
        response = self.client.get(self.HISTORY_LINK)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)         
    
    def test_get_list_recommendation_history_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.HISTORY_LINK)
        self.assertEqual(response.status_code, 401)

class HistoryDetailTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = AppUser.objects.create_user(email='email@email.com',username='testuser',password='test')
        self.another_user = AppUser.objects.create_user(email = 'anonymous@gmail.com', username='anonymous', password='test')
        
        self.client.force_authenticate(user=self.user)
        
        self.recommendation_attributes = {
            "user": self.user,
            "prompt": "Berikan rekomendasi tempat untuk acara ulang tahun di Braga, Bandung.",
            "output": "Berikut adalah 5 tempat makan favorit di Bandung.",
            "list": "[\"Tempat makan 1\", \"Tempat makan 2\", \"Tempat makan 3\"]",
            "keyword": "[\"Keyword 1\", \"Keyword 2\"]",
            "type": "specific"
        }
        self.model = RecommendationHistory.objects.create(**self.recommendation_attributes)
        self.serializer = RecommendationHistorySerializer(instance = self.model)
        self.HISTORY_DETAIL_LINK = reverse('ai:history-detail', kwargs={'id': str(self.model.id)})

    def test_get_detail_event(self):
        response = self.client.get(self.HISTORY_DETAIL_LINK)
        data = self.serializer.data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(data.keys()), set(response.data))
    
    def test_get_detail_event_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.HISTORY_DETAIL_LINK)
        self.assertEqual(response.status_code, 401)
        
class AutofillTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = AppUser.objects.create_user(email='email@email.com',username='testuser',password='test')
        self.another_user = AppUser.objects.create_user(email = 'anonymous@gmail.com', username='anonymous', password='test')
        
        self.client.force_authenticate(user=self.user)

    def test_autofill_valid(self):
        data = {
            'event' : {
                'name': 'Ulang tahun Ibu',
                'date': '26/02/2024',
                'budget': '300000',
                "objective": None,
                "attendees": None,
                "theme": "valentine",
                "services": None
            }
        }
        response = self.client.post(AUTOFILL_LINK, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(all(key in response.json().keys() for key in data['event'].keys()))

    def test_autofill_invalid(self):
        data = {
            'event' : {
                'name': None,
                'date': '26/02/2024',
                'budget': None,
                "objective": None,
                "attendees": None,
                "theme": "valentine",
                "services": None
            }
        }
        response = self.client.post(AUTOFILL_LINK, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['msg'], 'Make sure you fill the required fields.')

    def test_autofill_empty_input(self):
        data = {
            'event' : {
                'name': '',
                'date': '26/02/2024',
            }
        }
        response = self.client.post(AUTOFILL_LINK, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['msg'], 'Make sure you are putting a correct form data.')
