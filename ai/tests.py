from rest_framework.test import APIClient
from django.test import TestCase
from django.urls import reverse
from prompts import create_autofill_prompt
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

    def test_assistant_empty_input(self):
        data = {
            'prompt' : ', .',
        }
        response = self.client.post(ASSISTANT_LINK, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['msg'], 'Make sure you are putting a correct prompt to the assistant.')

class AutofillTest(TestCase):
    def SetUp(self):
        self.client = APIClient()

    def test_autofill_valid(self):
        form = {

        }
        data = {
            'prompt' : create_autofill_prompt(form),
        }
        response = self.client.post(AUTOFILL_LINK, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(all(key in response.json().keys() for key in ['objective', 'theme', 'service']))

    def test_autofill_invalid(self):
        form = {

        }
        data = {
            'prompt' : create_autofill_prompt(form),
        }
        response = self.client.post(AUTOFILL_LINK, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['msg'], 'Make sure you fill the required fields.')

    def test_autofill_empty_input(self):
        data = {
            'prompt' : ', .',
        }
        response = self.client.post(AUTOFILL_LINK, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['msg'], 'Make sure you are putting a correct prompt to the assistant.')
