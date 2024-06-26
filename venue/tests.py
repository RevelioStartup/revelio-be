from datetime import date
from decimal import Decimal
import json
from uuid import UUID
from django.urls import reverse
from django.db import IntegrityError
from django.forms import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from collections import OrderedDict
from rest_framework import status
from rest_framework.test import APIClient
from .models import Venue, PhotoVenue, Event
from .serializers import VenueSerializer
from utils.base_test import BaseTestCase

class BaseTestCaseVenue(BaseTestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.free_user)
        self.event_data = {
            "id": UUID("9fdfb487-5101-4824-8c3b-0775732aacda"),
            "user": self.free_user,
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
        self.venue_data = {
            "name": "Test Venue",
            "address": "123 Test St",
            "price": 50,
            "status": "PENDING",
            "contact_name": "John Doe",
            "contact_phone_number": "123-456-7890",
            "event_id": self.event_id,
        }
        self.venue = Venue.objects.create(**self.venue_data)

        self.venue1_data = {
            "name": "Venue 1",
            "address": "123 Test St",
            "price": 50,
            "status": "PENDING",
            "contact_name": "John Doe",
            "contact_phone_number": "123-456-7890",
            "event_id": self.event_id,
        }
        self.venue1 = Venue.objects.create(**self.venue1_data)

        self.venue2_data = {
            "name": "Venue 2",
            "address": "456 Test St",
            "price": 60,
            "status": "NONE",
            "contact_name": "Jane Doe",
            "contact_phone_number": "987-654-3210",
            "event_id": "9fdfb487-5101-4824-8c3b-0775732aacda",
        }
        self.venue2 = Venue.objects.create(**self.venue2_data)

class BaseTestCasePhoto(BaseTestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.free_user)
        self.event_data = {
            "id": UUID("9fdfb487-5101-4824-8c3b-0775732aacda"),
            "user": self.free_user,
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
        
        self.venue_data = {
            "name": "Test Venue",
            "address": "123 Test St",
            "price": 50,
            "status": "PENDING",
            "contact_name": "John Doe",
            "contact_phone_number": "1234567890",
            "event_id": "9fdfb487-5101-4824-8c3b-0775732aacda",
        }
        self.venue = Venue.objects.create(**self.venue_data)

        with open('empathymap.jpg', 'rb') as img:
            self.photo = PhotoVenue.objects.create(
                venue=self.venue,
                image=SimpleUploadedFile(img.name, img.read())
            )
            
        with open('empathymap.jpg', 'rb') as img:
            img_content = img.read()
            self.photo_data = {
                "venue": self.venue,
                "image": SimpleUploadedFile(img.name, img_content)
            }
            self.photo = PhotoVenue.objects.create(**self.photo_data)

class VenueModelTestCase(BaseTestCaseVenue):
    def test_venue_model(self):
        self.assertEqual(str(self.venue), "Test Venue")

    def test_venue_does_not_exist(self):
        non_existent_venue = Venue.objects.filter(name="Non Existent Venue").first()
        self.assertIsNone(non_existent_venue)

class VenueAPITestCase(BaseTestCaseVenue):
    def test_get_venue_list(self):
        url = reverse('venue-list-create')
        response = self.client.get(url)
        venues = Venue.objects.all()
        serializer = VenueSerializer(venues, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_venue(self):
        new_data = {"name": "Updated Venue", "address": "123 Test St", "price": 50, "status": "PENDING", "contact_name": "John Doe", "contact_phone_number": "123-456-7890", "event": self.event_id}
        url = reverse('venue-list-create')
        response = self.client.post(url, new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_venue_detail(self):
        url = reverse('venue-retrieve-update-destroy', args=[self.venue.id])
        response = self.client.get(url)
        serializer = VenueSerializer(self.venue)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_venue(self):
        url = reverse('venue-retrieve-update-destroy', args=[self.venue.id])
        updated_data = {"name": "Updated Venue", "address": "123 Test St", "price": 50, "status": "PENDING", "contact_name": "John Doe", "contact_phone_number": "123-456-7890", "event": self.event_id}
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

class VenueEventListViewTest(BaseTestCaseVenue):
    def test_get_venues_for_event(self):
        url = reverse('venue-event-list', kwargs={'event_id': "9fdfb487-5101-4824-8c3b-0775732aacda"})
        response = self.client.get(url)
        response_data = json.loads(json.dumps(response.data), object_pairs_hook=OrderedDict)
        expected_data = VenueSerializer([self.venue, self.venue1, self.venue2], many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, expected_data)
    
    def test_get_venues_for_event_no_venues(self):
        Venue.objects.all().delete()
        url = reverse('venue-event-list', kwargs={'event_id': "9fdfb487-5101-4824-8c3b-0775732aacda"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

class PhotoModelTestCase(BaseTestCasePhoto):
    def test_photo_model(self):
        self.assertTrue(str(self.photo).startswith('https://storage.googleapis.com/bucket-revelio-1'))

    def test_photo_model_no_venue(self):
        with self.assertRaises(IntegrityError):
            PhotoVenue.objects.create(
                venue=None,
                image=SimpleUploadedFile(name='empathymap.jpg', content=open('empathymap.jpg', 'rb').read())
            )

    def test_photo_model_no_image(self):
        with self.assertRaises(ValidationError):
            photo = PhotoVenue(venue=self.venue)
            photo.full_clean()

class PhotoAPITestCase(BaseTestCasePhoto):        
    def test_create_photo(self):
        url = reverse('photo-venue-create')
        self.photo_data['venue'] = self.venue.id
        with open('empathymap.jpg', 'rb') as img:
            self.photo_data['image'] = SimpleUploadedFile(img.name, img.read())
            response = self.client.post(url, self.photo_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_photo_detail(self):
        url = reverse('photo-venue-retrieve-update-destroy', args=[self.photo.id])
        response = self.client.get(url)
        self.assertTrue(self.photo.image.url.startswith('https://storage.googleapis.com/bucket-revelio-1'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_photo(self):
        url = reverse('photo-venue-retrieve-update-destroy', args=[self.photo.id])
        with open('empathymap.jpg', 'rb') as img:
            updated_data = {"venue": self.venue.id, "image": SimpleUploadedFile(img.name, img.read())}
            response = self.client.put(url, updated_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.photo.image.url.startswith('https://storage.googleapis.com/bucket-revelio-1'))

    def test_create_photo_missing_data(self):
        url = reverse('photo-venue-create')
        incomplete_data = {"venue": self.venue.id}
        response = self.client.post(url, incomplete_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_photo_detail_does_not_exist(self):
        url = reverse('photo-venue-retrieve-update-destroy', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_photo_does_not_exist(self):
        url = reverse('photo-venue-retrieve-update-destroy', args=[999])
        with open('empathymap.jpg', 'rb') as img:
            updated_data = {"venue": self.venue.id, "image": SimpleUploadedFile(img.name, img.read())}
            response = self.client.put(url, updated_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_photo(self):
        url = reverse('photo-venue-retrieve-update-destroy', args=[self.photo.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, {'pk': self.photo.pk})

    def test_delete_photo_does_not_exist(self):
        url = reverse('photo-venue-retrieve-update-destroy', args=[999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class VenueStatusUpdateAPITest(BaseTestCaseVenue):
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

