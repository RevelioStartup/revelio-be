from django.test import TestCase
from authentication.models import AppUser, Profile
from django.urls import reverse
import json
from django.core import mail
from rest_framework.test import APIClient
from .tokens import account_token
from django.core.files.uploadedfile import SimpleUploadedFile
import os

REGISTER_LINK = reverse('authentication:register')
LOGIN_LINK = reverse('authentication:login')
EMAIL_VERIFICATION_LINK = reverse('authentication:verify_email')
RECOVER_PASSWORD_LINK = reverse('authentication:recover_password')

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

    def test_login_successful(self):
        data = {'username': 'testuser', 'password': 'test'}
        response = self.client.post(LOGIN_LINK, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_login_failed(self):
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
        token = account_token.make_token(self.user)
        response = self.client.post((EMAIL_VERIFICATION_LINK), {'token': token})
        self.assertEqual(response.status_code, 200)
        user = AppUser.objects.get(pk=self.user.pk)
        self.assertTrue(user.is_verified_user)
    
    def test_invalid_verification_token(self):
        response = self.client.post((EMAIL_VERIFICATION_LINK), {'token': 'invalid token'})
        self.assertEqual(response.status_code, 400)

class SendRecoverPasswordEmailTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = AppUser.objects.create_user(email='email@email.com',username='testuser',password='test')
    
    def test_sent_email_recover_password(self):
        response = self.client.post((RECOVER_PASSWORD_LINK), {'email':'email@email.com'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1) 
        self.assertEqual(mail.outbox[0].to, ['email@email.com'])
    
    def test_sent_wrong_email_recover_password(self):
        response = self.client.post((RECOVER_PASSWORD_LINK), {'email':'wrong@email.com'})
        self.assertEqual(response.status_code, 400)
    
    def test_change_password(self):
        token = account_token.make_token(self.user)
        response = self.client.put((RECOVER_PASSWORD_LINK), 
                                    {'email':'email@email.com', 'token': token, 'new_password':'newpass'})
        self.assertEqual(response.status_code, 200)
    
    def test_change_password_wrong_email(self):
        token = account_token.make_token(self.user)
        response = self.client.put((RECOVER_PASSWORD_LINK), 
                                    {'email':'wrong@email.com', 'token': token, 'new_password':'newpass'})
        self.assertEqual(response.status_code, 400)
    
    def test_change_password_wrong_token(self):
        response = self.client.put((RECOVER_PASSWORD_LINK), 
                                    {'email':'email@email.com', 'token': 'wrong token', 'new_password':'newpass'})
        self.assertEqual(response.status_code, 400)

class ProfileUpdateTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = AppUser.objects.create_user(email='test@example.com', username='testuser', password='test')
        self.client.force_authenticate(user=self.user)
        self.profile = Profile.objects.create(user=self.user, bio='Old bio')

    def tearDown(self):
        # Clean up any resources created during the test
        Profile.objects.filter(user=self.user).delete()

    def test_update_profile_with_valid_data(self):
        # Test updating profile with valid data
        data = {'bio': 'New bio'}
        response = self.client.put(reverse('authentication:update_profile'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Profile.objects.get(user=self.user).bio, 'New bio')

    def test_update_profile_with_empty_data(self):
        # Test updating profile with empty data
        data = {'bio': ''}
        response = self.client.put(reverse('authentication:update_profile'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Profile.objects.get(user=self.user).bio, '')  # Ensure bio is empty

    def test_update_profile_picture(self):
        # Test uploading profile picture
        image_path = 'assets/logo.jpg'  # Update to the actual path
        with open(image_path, 'rb') as f:
            image = SimpleUploadedFile('image.jpg', f.read(), content_type='image/jpeg')
        data = {'profile_picture': image}
        response = self.client.put(reverse('authentication:update_profile'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Profile.objects.get(user=self.user).profile_picture)  # Ensure profile picture is uploaded
        
    def test_update_profile_with_invalid_data(self):
        # Test updating profile with invalid data (uploading an image as bio)
        image_path = 'assets/invalid_img.jpg'  # Update to the actual invalid image path
        with open(image_path, 'rb') as f:
            image = SimpleUploadedFile(os.path.basename(image_path), f.read(), content_type='image/jpeg')
        data = {'bio': 'New bio', 'profile_picture': image}
        response = self.client.put(reverse('authentication:update_profile'), data)
        self.assertEqual(response.status_code, 400)  # Expect a bad request response

    def test_update_profile_unauthenticated(self):
        # Test updating profile when unauthenticated
        self.client.logout()
        data = {'bio': 'New bio'}
        response = self.client.put(reverse('authentication:update_profile'), data)
        self.assertEqual(response.status_code, 401)  # Expect unauthorized response

    def test_update_profile_picture_unauthenticated(self):
        # Test uploading profile picture when unauthenticated
        self.client.logout()
        image_path = 'assets/logo.jpg'  # Update to the actual path
        with open(image_path, 'rb') as f:
            image = SimpleUploadedFile('image.jpg', f.read(), content_type='image/jpeg')
        data = {'profile_picture': image}
        response = self.client.put(reverse('authentication:update_profile'), data)
        self.assertEqual(response.status_code, 401)  # Expect unauthorized response
