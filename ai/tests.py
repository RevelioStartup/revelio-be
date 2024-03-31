from datetime import date
from rest_framework.test import APIClient
from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from ai.models import RecommendationHistory
from ai.serializers import RecommendationHistorySerializer
from authentication.models import AppUser
from event.models import Event
from task.models import Task
import json
from decimal import Decimal
from uuid import UUID

# Create your tests here.

ASSISTANT_LINK = reverse('ai:assistant')
AUTOFILL_LINK = reverse('ai:autofill')
OPEN_AI_MODULE = 'ai.views.OpenAI'

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
        self.mock_response = {'choices':[{'message': {'content': '{"output" : "Berikut adalah rekomendasi tempat untuk acara ulang tahun di Braga, Bandung", "list": ["Braga Art Cafe", "Filosofi Kopi", "We The Fork", "Warung asik", "Sweet Cantina"], "keyword" : ["Cafe Instagrammable Bandung", "Tempat makan Braga", "Cafe Braga nyaman"]}'} }]}

    @patch(OPEN_AI_MODULE)
    def test_assitant_valid(self, mock_openai):
        mock_openai.chat.completions.create.return_value = self.mock_response
        data = {
            'prompt' : 'Berikan rekomendasi tempat untuk acara ulang tahun di Braga, Bandung.',
            'type': 'specific',
            'event_id': str(self.event.id)
        }
        response = self.client.post(ASSISTANT_LINK, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
    
    @patch(OPEN_AI_MODULE)
    def test_assitant_specific_no_event(self, mock_openai):
        mock_openai.chat.completions.create.return_value = self.mock_response
        data = {
            'prompt' : 'Berikan rekomendasi tempat untuk acara ulang tahun di Braga, Bandung.',
            'type': 'specific'
        }
        response = self.client.post(ASSISTANT_LINK, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    @patch(OPEN_AI_MODULE)
    def test_assitant_valid_general(self, mock_openai):
        mock_openai.chat.completions.create.return_value = self.mock_response
        data = {
            'prompt' : 'Di mana letak Braga dari ITB bandung?',
            'type': 'general',
            'event_id': str(self.event.id)
        }
        response = self.client.post(ASSISTANT_LINK, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    @patch(OPEN_AI_MODULE)
    def test_assistant_empty_input(self, mock_openai):
        mock_openai.chat.completions.create.return_value = self.mock_response
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
        self.mock_response = {'choices': [{'message': {'content': '{"name": "Class meet", "date" = "26/02/2024", "budget":1000000, "objective" : "Meningkatkan keakraban pertemanan antar kelas", "attendees":400, "theme" : "Valentine", "services" :  ["stand makanan", "sound system", "MC"]}'} }]}

    @patch(OPEN_AI_MODULE)
    def test_autofill_valid(self, mock_openai):
        mock_openai.chat.completions.create.return_value = self.mock_response
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

    @patch(OPEN_AI_MODULE)
    def test_autofill_invalid(self, mock_openai):
        mock_openai.chat.completions.create.return_value = self.mock_response
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

    @patch(OPEN_AI_MODULE)
    def test_autofill_empty_input(self, mock_openai):
        mock_openai.chat.completions.create.return_value = self.mock_response
        data = {
            'event' : {
                'name': '',
                'date': '26/02/2024',
            }
        }
        response = self.client.post(AUTOFILL_LINK, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['msg'], 'Make sure you are putting a correct form data.')

class TaskStepsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = AppUser.objects.create_user(email='user@example.com', username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

        self.event = Event.objects.create(
            user=self.user,
            name="Mom's birthdat",
            date=date.today(),
            budget=Decimal('1000000.00'),
            objective="To celebrate mom's 45th birthday with family.",
            attendees=150,
            theme="Floral and nature",
            services=""
        )    
        self.task = Task.objects.create(title="Prepare everything", description="Prepare all needs for the birthday party", event=self.event)
        self.AI_TASK_STEPS_LINK_VALID = reverse('ai:ai-task-steps', kwargs={'task_id': self.task.id})
        self.AI_TASK_STEPS_LINK_INVALID = reverse('ai:ai-task-steps', kwargs={'task_id': 0})
        self.mock_response = {'choices': [{'message': {'content': '{"steps": [{"name": "Search photographer", "description":"Search photographer on social media"}, {"name": "Pay", "description":"Pay photographer before D-Day"}, {"name": "Contact the photographer", "description":"Contact the photographer to give briefing and discuss ideas"}, {"name": "Ask for copies", "description":"Request copies physically on CD and digitally through flash disk"}]}'} }]}

    @patch(OPEN_AI_MODULE)
    def test_ai_task_steps_valid(self, mock_openai):
        mock_openai.chat.completions.create.return_value = self.mock_response
        response = self.client.get(self.AI_TASK_STEPS_LINK_VALID)
        self.assertEqual(response.status_code, 200)
        response = response.json()
        self.assertTrue('task_id' in response)
        self.assertTrue('steps' in response)
        self.assertTrue(len(response['steps']) > 0)
        self.assertTrue('name' in response['steps'][0])
        self.assertTrue('description' in response['steps'][0])

    @patch(OPEN_AI_MODULE)
    def test_ai_task_steps_task_invalid(self, mock_openai):
        mock_openai.chat.completions.create.return_value = self.mock_response
        response = self.client.get(self.AI_TASK_STEPS_LINK_INVALID)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['msg'], 'Task not found.')
