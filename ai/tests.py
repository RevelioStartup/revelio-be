from rest_framework.test import APIClient
from django.test import TestCase
from django.urls import reverse
import json

# Create your tests here.

ASSISTANT_LINK = reverse('ai:assistant')
AUTOFILL_LINK = reverse('ai:autofill')

class AssistantTest(TestCase):
    def SetUp(self):
        self.client = APIClient()

    def test_assitant_valid(self):
        data = {
            'prompt' : 'Berikan rekomendasi tempat untuk acara ulang tahun di Braga, Bandung.',
        }
        response = self.client.post(ASSISTANT_LINK, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()['msg']) > 0)

    def test_empty_input(self):
        data = {
            'prompt' : ', .',
        }
        response = self.client.post(ASSISTANT_LINK, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['msg'], 'Make sure you are putting a correct prompt to the assistant.')
