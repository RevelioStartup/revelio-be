from django.db import IntegrityError
from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from authentication.models import AppUser
from .models import Venue, PhotoVenue
from .serializers import VenueSerializer, PhotoVenueSerializer


class BaseTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = AppUser.objects.create_user(email='email@email.com',username='testuser',password='test')
        self.client.force_authenticate(user=self.user)
        self.venue_data = {
            "name": "Test Venue",
            "address": "123 Test St",
            "price": 50,
            "status": "PENDING",
            "contact_name": "John Doe",
            "contact_phone_number": "123-456-7890",
            "event": 1,
        }
        self.venue = Venue.objects.create(**self.venue_data)

        self.event_id = 1

        self.venue1_data = {
            "name": "Venue 1",
            "address": "123 Test St",
            "price": 50,
            "status": "PENDING",
            "contact_name": "John Doe",
            "contact_phone_number": "123-456-7890",
            "event": self.event_id,
        }
        self.venue1 = Venue.objects.create(**self.venue1_data)

        self.photo = PhotoVenue.objects.create(
            venue=self.venue,
            image="https://example.com/path/to/your/image.jpg"
        )

        self.photo_data = {
            "venue": self.venue.id,
            "image": "https://example.com/path/to/your/image.jpg"
        }
        self.photo = PhotoVenue.objects.create(venue=self.venue, image=self.photo_data["image"])

class VenueModelTestCase(BaseTestCase):
    def test_venue_model(self):
        self.assertEqual(str(self.venue), "Test Venue")

    def test_venue_does_not_exist(self):
        non_existent_venue = Venue.objects.filter(name="Non Existent Venue").first()
        self.assertIsNone(non_existent_venue)

class VenueAPITestCase(BaseTestCase):
    def test_get_venue_list(self):
        url = reverse('venue-list-create')
        response = self.client.get(url)
        venues = Venue.objects.all()
        serializer = VenueSerializer(venues, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_venue(self):
        url = reverse('venue-list-create')
        response = self.client.post(url, self.venue_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_venue_detail(self):
        url = reverse('venue-retrieve-update-destroy', args=[self.venue.id])
        response = self.client.get(url)
        serializer = VenueSerializer(self.venue)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_venue(self):
        url = reverse('venue-retrieve-update-destroy', args=[self.venue.id])
        updated_data = {"name": "Updated Venue", "address": "123 Test St", "price": 50, "status": "PENDING", "contact_name": "John Doe", "contact_phone_number": "123-456-7890", "event": 1,}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Updated Venue")

    def test_delete_venue(self):
        url = reverse('venue-retrieve-update-destroy', args=[self.venue.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Venue.objects.filter(id=self.venue.id).exists())

    def test_get_venue_list_no_venues(self):
        Venue.objects.all().delete()
        url = reverse('venue-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_create_venue_missing_data(self):
        url = reverse('venue-list-create')
        incomplete_data = {"name": "Incomplete Venue"}
        response = self.client.post(url, incomplete_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_venue_detail_does_not_exist(self):
        url = reverse('venue-retrieve-update-destroy', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_venue_does_not_exist(self):
        url = reverse('venue-retrieve-update-destroy', args=[999])
        updated_data = {"name": "Updated Venue"}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_venue_does_not_exist(self):
        url = reverse('venue-retrieve-update-destroy', args=[999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class VenueEventListViewTest(BaseTestCase):
    def test_get_venues_for_event(self):
        url = reverse('venue-event-list', kwargs={'event_id': self.event_id})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        expected_data = VenueSerializer([self.venue, self.venue1], many=True).data
        self.assertEqual(response.data, expected_data)
    
    def test_get_venues_for_event_no_venues(self):
        Venue.objects.all().delete()
        url = reverse('venue-event-list', kwargs={'event_id': self.event_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

class PhotoModelTestCase(BaseTestCase):
    def test_photo_model(self):
        self.assertEqual(self.photo.venue, self.venue)
        self.assertEqual(str(self.photo), "https://example.com/path/to/your/image.jpg")

    def test_photo_model_no_venue(self):
        with self.assertRaises(IntegrityError):
            PhotoVenue.objects.create(
                venue=None,
                image="https://example.com/path/to/your/image.jpg"
            )

    def test_photo_model_no_image(self):
        with self.assertRaises(IntegrityError):
            PhotoVenue.objects.create(
                venue=self.venue,
                image=None
            )

class VenueStatusUpdateAPITest(BaseTestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = AppUser.objects.create_user(email='email@email.com',username='testuser',password='test')
        self.client.force_authenticate(user=self.user)
        self.venue = Venue.objects.create(name='Test Venue', address='Test Address', price=100, status='PENDING',
                                           contact_name='Test Contact', contact_phone_number='123456789', event=1)

    def test_venue_status_update(self):
        url = reverse('venue-status-update', kwargs={'pk': self.venue.pk})
        data = {'status': 'CONFIRMED'}  
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'CONFIRMED')

    def test_venue_status_update_invalid_venue_id(self):
        url = reverse('venue-status-update', kwargs={'pk': 999})  
        data = {'status': 'CONFIRMED'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_venue_status_update_invalid_status(self):
        url = reverse('venue-status-update', kwargs={'pk': self.venue.pk})
        data = {'status': 'INVALID_STATUS'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

