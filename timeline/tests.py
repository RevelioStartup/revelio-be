
from decimal import Decimal
import uuid
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from datetime import timedelta, date
from task.models import Task
from task_steps.models import TaskStep
from timeline.models import Timeline  
from event.models import Event 
from utils.base_test import BaseTestCase
from django.utils import timezone

class TimelineTestCase(BaseTestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.free_user)

        self.event = Event.objects.create(
            user=self.free_user,
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
            user=self.free_user
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
            user=self.free_user
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
            user=self.free_user
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
    
    def test_timeline_not_found(self):
        update_url = reverse('timeline-detail', kwargs={'pk': uuid.UUID('12345678-1234-5678-1234-567812345678')})
        
        response = self.client.patch(update_url, {
            "start_datetime": self.start_datetime.isoformat(),
            "end_datetime": self.end_datetime.isoformat(),
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    

class TimelineViewDeleteTestCase(BaseTestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.free_user)

        self.event = Event.objects.create(
            user=self.free_user,
            name="Annual Meeting",
            date=date.today(),
            budget=Decimal('20000.00'),
            objective="Discuss annual results and future plans.",
            attendees=100,
            theme="Corporate Blue",
            services="Catering, IT Support"
        )
        self.task = Task.objects.create(title="Setup Venue", description="Arranging chairs and tables", event=self.event)
        self.task_step = TaskStep.objects.create(
            name="Setup Tables",
            description="Arrange tables as per the layout",
            task=self.task,
            status='IN_PROGRESS',
            step_order=1,
            user=self.free_user
        )
        self.timeline = Timeline.objects.create(
            task_step=self.task_step,
            start_datetime=timezone.now() - timedelta(hours=2),
            end_datetime=timezone.now()
        )

    def test_delete_timeline(self):
        delete_url = reverse('timeline-delete', kwargs={'id': self.timeline.id})
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_non_existent_timeline(self):
        delete_url = reverse('timeline-delete', kwargs={'id': uuid.uuid4()})
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_related_data_integrity_post_deletion(self):
        delete_url = reverse('timeline-delete', kwargs={'id': self.timeline.id})
        self.client.delete(delete_url)
        self.assertTrue(Event.objects.filter(id=self.event.id).exists())
        self.assertTrue(Task.objects.filter(id=self.task.id).exists())


class TimelineListTestCase(BaseTestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.free_user)

        self.event1 = Event.objects.create(
            user=self.free_user, 
            name="Event 1", 
            date=timezone.now().date(),
            budget=Decimal('5000.00'),
            objective="To onboard new employees",
            attendees=100,
            theme="Harry",
            services="Catering, Decorations, Music"
        )
        self.event2 = Event.objects.create(
            user=self.free_user, 
            name="Event 2", 
            date=timezone.now().date(),
            budget=Decimal('3000.00'),
            objective="To onboard new employees",
            attendees=100,
            theme="Harry",
            services="Catering, Decorations, Music"
        )

        self.task1 = Task.objects.create(
            title="Task 1", 
            event=self.event1,
            description="This is a sample task description.",
            status="Not Started"
        )
        self.task2 = Task.objects.create(
            title="Task 2", 
            event=self.event2,
            description="This is a sample task description.",
            status="Not Started"
        )

        self.task_step1 = TaskStep.objects.create(
            name="Initial Step",
            description="Initial Description",
            task=self.task1,  # Here is the corrected reference
            status='NOT_STARTED',
            step_order=1,
            user=self.free_user
        )
        self.task_step2 = TaskStep.objects.create(
            name="Next Step",
            description="Initial Description",
            task=self.task2,  # Here is the corrected reference
            status='NOT_STARTED',
            step_order=2,
            user=self.free_user
        )

        self.timeline1 = Timeline.objects.create(
            task_step=self.task_step1, 
            start_datetime=timezone.now(), 
            end_datetime=timezone.now() + timedelta(hours=1)
        )
        self.timeline2 = Timeline.objects.create(
            task_step=self.task_step2, 
            start_datetime=timezone.now(), 
            end_datetime=timezone.now() + timedelta(hours=1)
        )

    def test_list_timelines_specific_event(self):
        url = reverse('event-timelines', kwargs={'event_id': self.event1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_timelines_no_event_timelines(self):
        event3 = Event.objects.create(
            user=self.free_user,
            name="Event 3",
            date=timezone.now().date(),
            budget=Decimal('2000.00'),  
            attendees=50,  
            objective="A new event with no timelines",
            theme="Minimal",
            services="Basic Services"
        )
        url = reverse('event-timelines', kwargs={'event_id': event3.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  

