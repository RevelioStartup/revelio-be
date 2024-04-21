
from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from datetime import datetime, timedelta, date
from task.models import Task
from task_steps.models import TaskStep
from authentication.models import AppUser
from timeline.models import Timeline  
from event.models import Event 

class TimelineCreateTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = AppUser.objects.create_user(email='user@example.com', username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

        self.event = Event.objects.create(
            user=self.user,
            name="Annual Gala",
            date=date.today(),
            budget=Decimal('10000.00'),
            objective="To celebrate the company's annual achievements.",
            attendees=150,
            theme="Futuristic",
            services="Catering, Security, Entertainment"
        )
        self.task = Task.objects.create(title="Task for Steps", description="Task Description", event=self.event)

        self.task_step = TaskStep.objects.create(
            name="Initial Step",
            description="Initial Description",
            task=self.task,
            status='NOT_STARTED',
            step_order=1,
            user=self.user
        )

        self.url = reverse('timeline-create')  # Make sure this name matches in urls.py

        self.start_datetime = datetime.now()
        self.end_datetime = datetime.now() + timedelta(hours=1)  # One hour later

    def test_create_timeline_success(self):
        data = {
            "task_step": str(self.task_step.id),
            "start_datetime": self.start_datetime.isoformat(),
            "end_datetime": self.end_datetime.isoformat(),
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Timeline.objects.count(), 1)
        self.assertTrue(Timeline.objects.filter(task_step=self.task_step).exists())

    def test_create_timeline_duplicate(self):
        # First creation
        Timeline.objects.create(task_step=self.task_step, start_datetime=self.start_datetime, end_datetime=self.end_datetime)
        
        # Duplicate attempt
        data = {
            "task_step": str(self.task_step.id),
            "start_datetime": self.start_datetime.isoformat(),
            "end_datetime": self.end_datetime.isoformat(),
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)  # Assuming your API sends this key on error

    def test_create_timeline_invalid_dates(self):
        data = {
            "task_step": str(self.task_step.id),
            "start_datetime": self.end_datetime.isoformat(),
            "end_datetime": self.start_datetime.isoformat(),
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)  

    def test_create_timeline_missing_fields(self):

        data = {
            "start_datetime": self.start_datetime.isoformat(),
            "end_datetime": self.end_datetime.isoformat(),
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)  
        
    def test_concurrent_timeline_creation(self):
        data = {
            "task_step": str(self.task_step.id),
            "start_datetime": self.start_datetime.isoformat(),
            "end_datetime": self.end_datetime.isoformat(),
        }
        # Simulate concurrent requests
        response1 = self.client.post(self.url, data, format='json')
        response2 = self.client.post(self.url, data, format='json')
        self.assertTrue(response1.status_code == status.HTTP_201_CREATED or response2.status_code == status.HTTP_201_CREATED)
        self.assertTrue(response1.status_code == status.HTTP_400_BAD_REQUEST or response2.status_code == status.HTTP_400_BAD_REQUEST)