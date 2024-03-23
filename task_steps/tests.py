from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from datetime import date
from task.models import Task
from event.models import Event  # Adjust this import based on your project structure
from task_steps.models import TaskStep
from authentication.models import AppUser

class TaskStepTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = AppUser.objects.create_user(email='user@example.com', username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

        # Ensure correct usage of Event model fields
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

        # Creating initial TaskSteps with a linked Task
        TaskStep.objects.create(name="Initial Step", output="Initial Output", description="Initial Description", status="NOT_STARTED", step_order=1, task=self.task)

    def test_get_task_steps(self):
        url = reverse('task-step-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Expecting 1 TaskStep based on setUp

    def test_create_task_step(self):
        url = reverse('task-step-list-create')
        data = {
            "name": "New Step",
            "output": "New Output",
            "description": "New Description",
            "status": "NOT_STARTED",
            "step_order": 2,
            "task": str(self.task.id)  # Ensure this matches the expected format (UUID/string)
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(TaskStep.objects.filter(name="New Step").exists())


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
        self.task = Task.objects.create(title="Sample Task", description="Sample Description", event=self.event)
        self.task_with_steps = Task.objects.create(title="Task With Steps", description="Has Steps", event=self.event)
        self.task_without_steps = Task.objects.create(title="Task Without Steps", description="No Steps", event=self.event)

        self.task_step1 = TaskStep.objects.create(
            name="Step 1", 
            output="Output 1", 
            description="Description 1", 
            status="NOT_STARTED", 
            step_order=1, 
            task=self.task_with_steps  # Associate with task_with_steps
        )
        self.task_step2 = TaskStep.objects.create(
            name="Step 2", 
            output="Output 2", 
            description="Description 2", 
            status="ON_PROGRESS", 
            step_order=2, 
            task=self.task_with_steps  # Associate with task_with_steps
        )

    def test_delete_single_task_step(self):
        url = reverse('task-step-detail', args=[self.task_step1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(TaskStep.objects.filter(id=self.task_step1.id).exists())

    def test_delete_all_task_steps_for_a_task(self):
        TaskStep.objects.filter(task=self.task).delete()
        self.assertFalse(TaskStep.objects.filter(task=self.task).exists())

    def test_delete_all_task_steps_for_a_task_with_steps(self):
        # Debugging: Print the count before deletion to confirm setup
        print("TaskSteps before deletion:", TaskStep.objects.filter(task=self.task_with_steps).count())

        url = reverse('delete-all-task-steps', args=[self.task_with_steps.id])
        response = self.client.delete(url)

        # Debugging: Print response data
        print("Response data:", response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(TaskStep.objects.filter(task=self.task_with_steps).exists())
        self.assertIn("Successfully deleted 2 task step(s).", response.data["message"])

    def test_delete_all_task_steps_for_a_task_without_steps(self):
        url = reverse('delete-all-task-steps', args=[self.task_without_steps.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(TaskStep.objects.filter(task=self.task_without_steps).exists())
        self.assertIn("Successfully deleted 0 task step(s).", response.data["message"])
