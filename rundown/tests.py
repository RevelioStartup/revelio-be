from datetime import date
from decimal import Decimal
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from authentication.models import AppUser
from .models import Event, Rundown
import datetime
from django.contrib.auth.models import BaseUserManager
from utils.base_test import BaseTestCase

class RundownBaseTestCase(BaseTestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.free_user)

        self.event_data = {
            "user": self.free_user,
            "name": "Revelio Onboarding",
            "date": date.today(),
            "budget": Decimal('20000000'),
            "objective": "To onboard new employees",
            "attendees": 100,
            "theme": "Harry Potter",
            "services": "Catering, Decorations, Music"
        }
        self.event = Event.objects.create(**self.event_data)
        self.event_id = self.event.id

        self.rundown_data = {
            "event_id": self.event_id,  
            "rundown_data": [
                {
                    "description": "Acara 1",
                    "start_time": "08:00",
                    "end_time": "09:00"
                },
                {
                    "description": "Acara 2",
                    "start_time": "09:00",
                    "end_time": "09:30"
                },
                {
                    "description": "Acara 3",
                    "start_time": "10:00",
                    "end_time": "10:30"
                }
            ]
        }


class CreateRundownTestCase(RundownBaseTestCase):

    url = reverse('rundown-create')

    def test_create_rundown_successfully(self):
        response = self.client.post(self.url, self.rundown_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_rundown_invalid_data(self):
        invalid_rundown_data = {
            "event_id": self.event_id,  # Use the dynamic event ID
            "rundown_data": [
                {
                    "description": "Acara 1",
                    "start_time": "08:00",
                    "end_time": "09:00"
                },
                {
                    "description": "Acara 2",
                    "start_time": "08:00",
                    "end_time": "09:30"
                }
            ]
        }
        response = self.client.post(self.url, invalid_rundown_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_rundown_already_created(self):
        response = self.client.post(self.url, self.rundown_data, format='json')
        response = self.client.post(self.url, self.rundown_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateRundownTestCase(RundownBaseTestCase):

    def set_up_rundown(self):
        self.rundown_1 = Rundown.objects.create(
            event=self.event,
            rundown_order=1,
            description="Acara 1",
            start_time=datetime.time(8,0),
            end_time=datetime.time(9,0),
        )
        self.rundown_2 = Rundown.objects.create(
            event=self.event,
            rundown_order=2,
            description="Acara 2",
            start_time=datetime.time(9,0),
            end_time=datetime.time(9,30),
        )

    def test_update_rundown_successfully(self):
        self.set_up_rundown()
        updated_rundown_data={
                "description":"Acara 2 Updated",
                "start_time":"09:10",
                "end_time":"09:30"
        }
        url = reverse('rundown-detail', args=[self.rundown_2.id])
        response = self.client.patch(url, updated_rundown_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_rundown_invalid_data(self):
        self.set_up_rundown()
        updated_rundown_data_invalid={
                "description":"Acara 2 Updated",
                "start_time":"08:10",
                "end_time":"09:30"
        }
        url = reverse('rundown-detail', args=[self.rundown_2.id])
        response = self.client.patch(url, updated_rundown_data_invalid, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        updated_rundown_data_invalid_2={
                "description":"Acara 1 Updated",
                "start_time":"08:10",
                "end_time":"11:30"
        }
        url = reverse('rundown-detail', args=[self.rundown_1.id])
        response = self.client.patch(url, updated_rundown_data_invalid_2, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        updated_rundown_data_invalid_3={
                "description":"Acara 1 Updated",
                "start_time":"18:10",
                "end_time":"11:30"
        }
        url = reverse('rundown-detail', args=[self.rundown_1.id])
        response = self.client.patch(url, updated_rundown_data_invalid_3, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class GetRundownListTestCase(RundownBaseTestCase):
    url = reverse('rundown-create')

    def test_get_rundown_list(self):
        self.client.post(self.url, self.rundown_data, format='json')
        url = reverse('rundown-list', args=[self.event_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["description"], "Acara 1")

    def test_no_rundown(self):
        url = reverse('rundown-list', args=[self.event_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_not_rundown_owner(self):
        self.client = APIClient()
        invalid_owner_password = BaseUserManager().make_random_password()
        self.user = AppUser.objects.create_user(email='invalid@email.com', username='invalid', password=invalid_owner_password)
        self.client.force_authenticate(user=self.user)
        url = reverse('rundown-list', args=[self.event_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class DeleteRundownTestCase(RundownBaseTestCase):
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

    def test_delete_single_rundown(self):
        self.set_up_rundown()
        url = reverse('rundown-detail', args=[self.rundown_2.id])  
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        self.assertFalse(Rundown.objects.filter(id=self.rundown_2.id).exists())

    def test_delete_all_task_steps_for_a_task(self):
        url = reverse('rundown-delete-all', args=[self.event.id])  
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        self.assertFalse(Rundown.objects.filter(event=self.event).exists())