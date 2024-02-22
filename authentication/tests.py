from django.test import TestCase, Client
from authentication.models import *
from django.urls import reverse
import json

class RegisterTest(TestCase):
    def setUp(self):
        self.client = Client()

    def testRegisterValid(self):
        data = {
                "username":"user1",
                "password":"pass1",
                "email":"email1@email.com"
        }
        response = self.client.post(reverse('authentication:register'), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(AppUser.objects.filter(username='user1').exists())