from datetime import date
from decimal import Decimal
from uuid import UUID
from django.test import TestCase
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from authentication.models import AppUser
from .models import Task, Event
from .serializers import TaskSerializer

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

        self.task_data = {
            "title": "Task Default",
            "description": "This is a description of task default",
            "status": "Not Started",
            "event_id": self.event_id,
        }
        self.task = Task.objects.create(**self.task_data)

class TaskModelTestCase(BaseTestCase):
    def test_task_model(self):
        self.assertEqual(str(self.task), "Task Default")

    def test_task_does_not_exist(self):
        non_existent_task = Task.objects.filter(title="Non Existent Task").first()
        self.assertIsNone(non_existent_task)

class TaskAPITestCase(BaseTestCase):
    def test_create_task(self):
        new_data = {
            "title": "Updated Task",
            "description": "This is a description of the updated task",
            "status": "On Progress",
            "event": self.event_id,
        }
        url = reverse('task-create')
        response = self.client.post(url, new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_task_missing_data(self):
        url = reverse('task-create')
        incomplete_data = {"title": "Incomplete Vendor"}
        response = self.client.post(url, incomplete_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
class SeeTaskListViewTestCase(BaseTestCase):
    
    def test_get_tasks_list(self):
        task_data_2 = {
            "title": "Task Default 2 ",
            "description": "This is a description of task default 2",
            "status": "Not Started",
            "event_id": self.event_id,
        }
        task2 = Task.objects.create(**task_data_2)
        url = reverse('get-task-list', args=[self.event_id])
        data = TaskSerializer([self.task, task2], many=True).data
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)
    
    def test_get_task_list_no_task(self):
        Task.objects.all().delete()
        url = reverse('get-task-list', args=[self.event_id])
        data = []
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)

class UpdateTaskViewTestCase(BaseTestCase):
    def test_update_task(self):
        new_data = {
            "title": "Updated Task",
            "description": "This is a description of the updated task",
            "status": "On Progress",
            "event_id": self.event_id,
        }
        url = reverse('update-task', args=[self.event_id, self.task.pk])
        response = self.client.patch(url, new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_update_task_not_found(self):
        url = reverse('update-task', args=[UUID("9fdfb487-5101-4824-8c3b-0775732aacdb"), self.task.pk])
        response = self.client.patch(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_update_task_invalid_data(self):
        url = reverse('update-task', args=[self.event_id, self.task.pk])
        response = self.client.patch(url, {"status": "not_on_progress"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)