
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
from django.utils import timezone

class TimelineTestCase(TestCase):
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
            step_order=2,
            user=self.user
        )

        self.url = reverse('timeline-create') 

        self.current_timezone = timezone.get_current_timezone()
        self.start_datetime = timezone.localtime(timezone.now(), timezone=self.current_timezone)
        self.end_datetime = timezone.localtime(timezone.now() + timedelta(hours=1), timezone=self.current_timezone)

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
        Timeline.objects.create(task_step=self.task_step, start_datetime=self.start_datetime, end_datetime=self.end_datetime)
        
        data = {
            "task_step": str(self.task_step.id),
            "start_datetime": self.start_datetime.isoformat(),
            "end_datetime": self.end_datetime.isoformat(),
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)  

    def test_create_timeline_invalid_dates(self):
        data = {
            "task_step": str(self.task_step.id),
            "start_datetime": self.end_datetime.isoformat(),
            "end_datetime": self.start_datetime.isoformat(),
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)  
    

    def test_invalid_step_order_larger(self):
        Timeline.objects.create(task_step=self.task_step, start_datetime=self.start_datetime, end_datetime=self.end_datetime)
        larger_step = TaskStep.objects.create(
            name="Higher Step",
            description="Higher Description",
            task=self.task,
            status='NOT_STARTED',
            step_order=3,  
            user=self.user
        )
        small_start_datetime = timezone.localtime(timezone.now(), timezone=self.current_timezone) - timedelta(hours=1)
        small_end_datetime = timezone.localtime(timezone.now(), timezone=self.current_timezone)
        data = {
            "task_step": str(larger_step.id),
            "start_datetime": small_start_datetime.isoformat(),
            "end_datetime": small_end_datetime.isoformat(),
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertIn("A task step with a larger step order cannot precede a task step with a smaller step order.", response.data["error"])

    def test_invalid_step_order_smaller(self):
        Timeline.objects.create(task_step=self.task_step, start_datetime=self.start_datetime, end_datetime=self.end_datetime)
        smaller_step = TaskStep.objects.create(
            name="Smaller Step",
            description="Higher Description",
            task=self.task,
            status='NOT_STARTED',
            step_order=1,  
            user=self.user
        )
        large_start_datetime = timezone.localtime(timezone.now(), timezone=self.current_timezone) + timedelta(hours=1)
        large_end_datetime = timezone.localtime(timezone.now(), timezone=self.current_timezone)  + timedelta(hours=2)
        data = {
            "task_step": str(smaller_step.id),
            "start_datetime": large_start_datetime.isoformat(),
            "end_datetime": large_end_datetime.isoformat(),
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertIn("A task step with a smaller step order cannot follow a task step with a larger step order.", response.data["error"])
        
    def test_update_detail_timeline_success(self):
        new_starttime = timezone.localtime(timezone.now() + + timedelta(hours=2), timezone=self.current_timezone)
        new_endtime = timezone.localtime(timezone.now() + timedelta(hours=3), timezone=self.current_timezone)
        
        created_timeline = self.client.post(self.url,                
            {
                "task_step": str(self.task_step.id),
                "start_datetime": self.start_datetime.isoformat(),
                "end_datetime": self.end_datetime.isoformat(),
            }, format='json')
        
        timeline_id = created_timeline.data['id']
        
        update_url = reverse('timeline-detail', kwargs={'pk': timeline_id})
        
        response = self.client.patch(update_url, {
            "start_datetime": new_starttime.isoformat(),
            "end_datetime": new_endtime.isoformat(),
        }, format='json')

        self.assertIn('start_datetime', response.data)
        self.assertIn('end_datetime', response.data)
        
    def test_update_detail_timeline_invalid_date(self):
        new_starttime = timezone.localtime(timezone.now() + + timedelta(hours=2), timezone=self.current_timezone)
        new_endtime = timezone.localtime(timezone.now() + timedelta(hours=3), timezone=self.current_timezone)
        
        created_timeline = self.client.post(self.url,                
            {
                "task_step": str(self.task_step.id),
                "start_datetime": self.start_datetime.isoformat(),
                "end_datetime": self.end_datetime.isoformat(),
            }, format='json')
        
        timeline_id = created_timeline.data['id']
        
        update_url = reverse('timeline-detail', kwargs={'pk': timeline_id})
        
        response = self.client.patch(update_url, {
            "start_datetime": new_endtime.isoformat(),
            "end_datetime": new_starttime.isoformat(),
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    