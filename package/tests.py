from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from authentication.models import AppUser
from .models import Package

class PackageRetrieveAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = AppUser.objects.create_user(email='email@email.com', username='testuser', password='test')
        self.client.force_authenticate(user=self.user)

        self.package1 = Package.objects.create(
            name='Free',
            price=0,
            duration=0,
            event_planner=True,
            event_tracker=True,
            event_timeline=True,
            event_rundown=True,
            ai_assistant=False
        )
        self.package2 = Package.objects.create(
            name='Premium',
            price=10000,
            duration=30,
            event_planner=True,
            event_tracker=True,
            event_timeline=True,
            event_rundown=True,
            ai_assistant=True
        )

    def test_retrieve_package(self):
        url = reverse('package-detail', kwargs={'id': self.package1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.package1.id)
        self.assertEqual(response.data['name'], 'Free')

        url = reverse('package-detail', kwargs={'id': self.package2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.package2.id)
        self.assertEqual(response.data['name'], 'Premium')

    def test_retrieve_package_invalid_id(self):
        url = reverse('package-detail', kwargs={'id': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
