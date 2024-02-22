from django.test import TestCase, Client
from authentication.models import *
from django.urls import reverse
import json

REGISTER_LINK = reverse('authentication:register')
LOGIN_LINK = reverse('authentication:login')

class RegisterTest(TestCase):

    def setUp(self):
        self.client = Client()

    def testRegisterValid(self):
        data = {
                "username":"user1",
                "password":"pass1",
                "email":"email1@email.com"
        }
        response = self.client.post(REGISTER_LINK, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(AppUser.objects.filter(username='user1').exists())
    
    def testEmailFormatNotValid(self):
        data ={
                "username":"user1",
                "password":"pass1",
                "email":"emailnotvalid"
        }
        response = self.client.post(REGISTER_LINK, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['msg'],"Email format is wrong.")
        self.assertFalse(AppUser.objects.filter(username='user1').exists())
    
    def testEmptyInput(self):
        data = {
                "username":"",
                "password":"",
                "email":""
        }
        response = self.client.post(REGISTER_LINK, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['msg'],"Empty input! Make sure all the fields are filled.")
    
    def testUsernameIsAlreadyExist(self):
        data = {
                "username":"user1",
                "password":"pass1",
                "email":"email1@email.com"
        }
        response = self.client.post(REGISTER_LINK, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response = self.client.post(REGISTER_LINK, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['msg'],"Username and/or email already taken!")

class LoginTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = AppUser.objects.create_user(email='email@email.com',username='testuser',password='test')

    def testLoginSuccessful(self):
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(LOGIN_LINK, data=data)
        self.assertEqual(response.status_code, 200)    