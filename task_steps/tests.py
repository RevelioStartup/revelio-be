from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from datetime import date
from task.models import Task
from event.models import Event
from task_steps.models import TaskStep
from authentication.models import AppUser

class TaskStepCreateTestCase(TestCase):
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

    def test_create_task_steps(self):
        url = reverse('task-step-create') 
        data = {
            "task_id": self.task.id, 
            "steps": [
                {"name": "Step 1", "description": "Description 1"},
                {"name": "Step 2", "description": "Description 2"}
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TaskStep.objects.filter(task=self.task).count(), 2)
        self.assertTrue(TaskStep.objects.filter(name="Step 1", task=self.task).exists())
        self.assertTrue(TaskStep.objects.filter(name="Step 2", task=self.task).exists())

    def test_create_task_steps_for_existing_task(self):
        url = reverse('task-step-create')
        self.client.post(url, {
            "task_id": self.task.id,
            "steps": [{"name": "Initial Step", "description": "Initial Step Description"}]
        }, format='json')
        data = {
            "task_id": self.task.id,
            "steps": [{"name": "Another Step", "description": "Another Step Description"}]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Task steps for the specified task already exist.")

    def test_create_task_steps_invalid_data(self):
        url = reverse('task-step-create')
        data = {
            "task_id": self.task.id,
            "steps": [{"description": "Missing name field"}]  
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("errors", response.data)

    def test_get_task_steps_wrong_method(self):
        url = reverse('task-step-create')  
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

class TaskStepUpdateTestCase(TestCase):
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
            status="NOT_STARTED",
            step_order=1,
            task=self.task,
            user=self.user
        )
    
    def test_update_task_step(self):
        url = reverse('task-step-update', kwargs={'pk': self.task_step.id}) 
        data = {
            "name": "Updated Step",
            "description": "Updated Description",
            "status": "DONE",
            "step_order": self.task_step.step_order,
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(TaskStep.objects.filter(name="Updated Step").exists())
        updated_task_step = TaskStep.objects.get(id=self.task_step.id)
        self.assertEqual(updated_task_step.name, "Updated Step")
        self.assertEqual(updated_task_step.description, "Updated Description")
        self.assertEqual(updated_task_step.status, "DONE")

    def test_update_task_step_2(self):
        url = reverse('task-step-update', kwargs={'pk': self.task_step.id}) 
        data = {
            "name": "Updated Step",
            "description": "Updated Description",
            "status": "ON_PROGRESS",
            "step_order": self.task_step.step_order,
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_task_step_3(self):
        url = reverse('task-step-update', kwargs={'pk': self.task_step.id}) 
        data = {
            "name": "Updated Step",
            "description": "Updated Description",
            "status": "NOT_STARTED",
            "step_order": self.task_step.step_order,
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_invalid(self):
        url = reverse('task-step-update', kwargs={'pk': self.task_step.id}) 
        data = {
            "nam": "Updated Step",
            "descripion": "Updated Description",
            "statu": "DONE",
            "step_orde": self.task_step.step_order,
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_update_status_invalid(self):
        url = reverse('task-step-update', kwargs={'pk': self.task_step.id}) 
        data = {
            "name": "Updated Step",
            "description": "Updated Description",
            "status": "dummy",
            "step_order": self.task_step.step_order,
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class TaskStepAppendTestCase(TestCase):
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
        self.task = Task.objects.create(title="Task for Steps", description="Task Description", event=self.event, status='Done')

        self.task_step = TaskStep.objects.create(
            name="Initial Step",
            description="Initial Description",
            status="DONE",
            step_order=1,
            task=self.task,
            user=self.user
        )
    
    def test_append_task_valid(self):
        url = reverse('append-task-step', kwargs={'task_id': self.task.id}) 
        data = {
            "name": "append step",
            "description": "append step",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        steps = TaskStep.objects.filter(task=self.task.id)
        self.assertTrue(len(steps) == 2)

class TaskStepDeletionTestCase(TestCase):
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
            status="NOT_STARTED",
            step_order=1,
            task=self.task,
            user=self.user 
        )

    def test_delete_single_task_step(self):
        url = reverse('task-step-detail', args=[self.task_step.id])  
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        self.assertFalse(TaskStep.objects.filter(id=self.task_step.id).exists())

    def test_delete_all_task_steps_for_a_task(self):
        url = reverse('delete-all-task-steps', args=[self.task.id])  
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        self.assertFalse(TaskStep.objects.filter(task=self.task).exists())