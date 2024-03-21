from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import TaskStep
from authentication.models import AppUser

class TaskStepTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = AppUser.objects.create_user(email='user@example.com', username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

        TaskStep.objects.create(name="Step 1", output="Output 1", description="Description 1", status="NOT_STARTED", step_order=1)
        TaskStep.objects.create(name="Step 2", output="Output 2", description="Description 2", status="ON_PROGRESS", step_order=2)

    def test_get_task_steps(self):
        url = reverse('task-step-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Expecting 2 TaskSteps

    def test_create_task_step(self):
        url = reverse('task-step-list-create')
        data = {
            "name": "Step 3",
            "output": "Output 3",
            "description": "Description 3",
            "status": "DONE",
            "step_order": 3
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TaskStep.objects.count(), 3)  


        task_step = TaskStep.objects.get(name="Step 3")
        self.assertEqual(task_step.output, "Output 3")
        self.assertEqual(task_step.description, "Description 3")
        self.assertEqual(task_step.status, "DONE")
        self.assertEqual(task_step.step_order, 3)
