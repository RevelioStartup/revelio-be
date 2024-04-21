from datetime import date
from decimal import Decimal
from uuid import UUID
from django.test import TestCase
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from authentication.models import AppUser
from .models import Event, Rundown
import datetime

class BaseTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = AppUser.objects.create_user(email='email@email.com', username='testuser', password='test')
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
        self.event_id = UUID("9fdfb487-5101-4824-8c3b-0775732aacda")

        self.rundown_data = {
            "event_id":UUID("9fdfb487-5101-4824-8c3b-0775732aacda"),
            "rundown_data":[
                {
                    "description":"Acara 1",
                    "start_time":"08:00",
                    "end_time":"09:00"
                },
                {
                    "description":"Acara 2",
                    "start_time":"09:00",
                    "end_time":"09:30"
                },
                {
                    "description":"Acara 3",
                    "start_time":"10:00",
                    "end_time":"10:30"
                }
            ]
        }

class CreateRundownTestCase(BaseTestCase):

    url = reverse('rundown-create')

    def test_create_rundown_successfully(self):
        response = self.client.post(self.url, self.rundown_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_rundown_invalid_data(self):
        invalid_rundown_data = {
            "event_id":UUID("9fdfb487-5101-4824-8c3b-0775732aacda"),
            "rundown_data":[
                {
                    "description":"Acara 1",
                    "start_time":"08:00",
                    "end_time":"09:00"
                },
                {
                    "description":"Acara 2",
                    "start_time":"08:00",
                    "end_time":"09:30"
                }
            ]
        }
        response = self.client.post(self.url, invalid_rundown_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_rundown_already_created(self):
        response = self.client.post(self.url, self.rundown_data, format='json')
        response = self.client.post(self.url, self.rundown_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UpdateRundownTestCase(BaseTestCase):

    def set_up_rundown(self):
        self.rundown_1 = Rundown.objects.create(
            event = self.event,
            rundown_order = 1,
            description = "Acara 1",
            start_time = datetime.time(8,0),
            end_time = datetime.time(9,0),
        )
        self.rundown_2 = Rundown.objects.create(
            event = self.event,
            rundown_order = 2,
            description = "Acara 2",
            start_time = datetime.time(9,0),
            end_time = datetime.time(9,30),
        )

    def test_update_rundown_successfully(self):
        self.set_up_rundown()
        updated_rundown_data={
                "description":"Acara 2 Updated",
                "start_time":"09:10",
                "end_time":"09:30"
        }
        url = reverse('rundown-update', args=[self.rundown_2.id])
        response = self.client.patch(url, updated_rundown_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_rundown_invalid_data(self):
        self.set_up_rundown()
        updated_rundown_data_invalid={
                "description":"Acara 2 Updated",
                "start_time":"08:10",
                "end_time":"09:30"
        }
        url = reverse('rundown-update', args=[self.rundown_2.id])
        response = self.client.patch(url, updated_rundown_data_invalid, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        updated_rundown_data_invalid_2={
                "description":"Acara 1 Updated",
                "start_time":"08:10",
                "end_time":"11:30"
        }
        url = reverse('rundown-update', args=[self.rundown_1.id])
        response = self.client.patch(url, updated_rundown_data_invalid_2, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        updated_rundown_data_invalid_3={
                "description":"Acara 1 Updated",
                "start_time":"18:10",
                "end_time":"11:30"
        }
        url = reverse('rundown-update', args=[self.rundown_1.id])
        response = self.client.patch(url, updated_rundown_data_invalid_3, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        

