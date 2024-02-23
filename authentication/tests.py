from django.test import TestCase
from authentication.models import AppUser
from django.urls import reverse
import json
from django.core import mail
from rest_framework.test import APIClient
from .tokens import account_activation_token

REGISTER_LINK = reverse('authentication:register')
LOGIN_LINK = reverse('authentication:login')
EMAIL_VERIFICATION_LINK = reverse('authentication:verify_email')

class RegisterTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_register_valid(self):
        data = {
                "username":"user1",
                "password":"pass1",
                "email":"email1@email.com"
        }
        response = self.client.post(REGISTER_LINK, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(AppUser.objects.filter(username='user1').exists())
    
    def test_email_format_not_valid(self):
        data ={
                "username":"user1",
                "password":"pass1",
                "email":"emailnotvalid"
        }
        response = self.client.post(REGISTER_LINK, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['msg'],"Email format is wrong.")
        self.assertFalse(AppUser.objects.filter(username='user1').exists())
    
    def test_empty_input(self):
        data = {
                "username":"",
                "password":"",
                "email":""
        }
        response = self.client.post(REGISTER_LINK, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['msg'],"Empty input! Make sure all the fields are filled.")
    
    def test_username_is_already_exist(self):
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
        self.client = APIClient()
        self.user = AppUser.objects.create_user(email='email@email.com',username='testuser',password='test')

    def testLoginSuccessful(self):
        data = {'username': 'testuser', 'password': 'test'}
        response = self.client.post(LOGIN_LINK, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def testLoginFailed(self):
        data = {'username': 'testuser', 'password': 'testwrongpassword'}
        response = self.client.post(LOGIN_LINK, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['msg'],"Wrong username/password!") 

class SendVerificationEmailTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = AppUser.objects.create_user(email='email@email.com',username='testuser',password='test')
        self.client.force_authenticate(user=self.user)
    
    def test_sent_email(self):
        response = self.client.get(EMAIL_VERIFICATION_LINK)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1) 
        self.assertEqual(mail.outbox[0].to, ['email@email.com'])
    
    def test_valid_verification_token(self):
        token = account_activation_token.make_token(self.user)
        response = self.client.post((EMAIL_VERIFICATION_LINK), {'token': token})
        self.assertEqual(response.status_code, 200)
        user = AppUser.objects.get(pk=self.user.pk)
        self.assertTrue(user.is_verified_user)
    
    def test_invalid_verification_token(self):
        response = self.client.post((EMAIL_VERIFICATION_LINK), {'token': 'invalid token'})
        self.assertEqual(response.status_code, 400)