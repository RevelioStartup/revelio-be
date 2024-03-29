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

class TaskStepTestCase(TestCase):
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
            output="Initial Output",
            description="Initial Description",
            status="NOT_STARTED",
            step_order=1,
            task=self.task,
            user=self.user  # Ensure the task step is associated with the user
        )

    def test_get_task_steps(self):
        url = reverse('task-step-list-create')  # Ensure this is the correct name for your URL
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Expecting 1 TaskStep based on setUp

    def test_create_task_step(self):
        url = reverse('task-step-list-create')  # Ensure this is the correct name for your URL
        data = {
            "name": "New Step",
            "output": "New Output",
            "description": "New Description",
            "status": "NOT_STARTED",
            "step_order": 2,
            "task": self.task.id  # Directly use the task ID
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(TaskStep.objects.filter(name="New Step").exists())

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
            output="Initial Output",
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
            "output": "Updated Output",
            "description": "Updated Description",
            "status": "DONE",
            "step_order": self.task_step.step_order,
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(TaskStep.objects.filter(name="Updated Step").exists())
        updated_task_step = TaskStep.objects.get(id=self.task_step.id)
        self.assertEqual(updated_task_step.name, "Updated Step")
        self.assertEqual(updated_task_step.output, "Updated Output")
        self.assertEqual(updated_task_step.description, "Updated Description")
        self.assertEqual(updated_task_step.status, "DONE")

    def test_update_invalid(self):
        url = reverse('task-step-update', kwargs={'pk': self.task_step.id}) 
        data = {
            "nam": "Updated Step",
            "outpu": "Updated Output",
            "description": "Updated Description",
            "statu": "DONE",
            "step_orde": self.task_step.step_order,
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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
            output="Initial Output",
            description="Initial Description",
            status="NOT_STARTED",
            step_order=1,
            task=self.task,
            user=self.user  # Ensure the task step is associated with the user
        )

    def test_delete_single_task_step(self):
        url = reverse('task-step-detail', args=[self.task_step.id])  # Ensure this is the correct name for your URL
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(TaskStep.objects.filter(id=self.task_step.id).exists())

    def test_delete_all_task_steps_for_a_task(self):
        url = reverse('delete-all-task-steps', args=[self.task.id])  # Ensure this is the correct name for your URL
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(TaskStep.objects.filter(task=self.task).exists())
        # Note: You might need to adjust the response validation based on the actual response content
