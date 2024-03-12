from datetime import date
from rest_framework.test import APIClient
from django.test import TestCase
from django.urls import reverse
from ai.models import RecommendationHistory
from ai.serializers import RecommendationHistorySerializer
from authentication.models import AppUser
import json

# Create your tests here.

ASSISTANT_LINK = reverse('ai:assistant')
AUTOFILL_LINK = reverse('ai:autofill')
HISTORY_LINK = reverse('ai:history')

class AssistantTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = AppUser.objects.create_user(email='email@email.com',username='testuser',password='test')
        self.another_user = AppUser.objects.create_user(email = 'anonymous@gmail.com', username='anonymous', password='test')
        
        self.client.force_authenticate(user=self.user)

    def test_assitant_valid(self):
        data = {
            'prompt' : 'Berikan rekomendasi tempat untuk acara ulang tahun di Braga, Bandung.',
            'type': 'specific',
             "event": {
                "name": "Revelio Onboarding",
                "theme": "Sports"
            }
        }
        response = self.client.post(ASSISTANT_LINK, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
    
    def test_assitant_valid_general(self):
        data = {
            'prompt' : 'Di mana letak Braga dari ITB bandung?',
            'type': 'general',
                    "event": {
                "name": "Revelio Onboarding",
                "theme": "Sports"
            }
        }
        response = self.client.post(ASSISTANT_LINK, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_assistant_empty_input(self):
        data = {
            'prompt' : ', .',
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

    def test_get_list_recommendation_history(self):
        response = self.client.get(HISTORY_LINK)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)         
    
    def test_get_list_recommendation_history_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(HISTORY_LINK)
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
        self.HISTORY_DETAIL_LINK = reverse('ai:history-detail', kwargs={'id': self.model.id})

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
