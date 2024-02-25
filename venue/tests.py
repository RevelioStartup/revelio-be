from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from authentication.models import AppUser
from .models import Venue, Photo
from .serializers import VenueSerializer, PhotoSerializer

class VenueModelTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = AppUser.objects.create_user(email='email@email.com',username='testuser',password='test')
        self.client.force_authenticate(user=self.user)
        self.venue = Venue.objects.create(
            name="Test Venue",
            address="123 Test St",
            price=50,
            status="Active",
            contact_name="John Doe",
            contact_phone_number="123-456-7890",
            event=1,
        )

    def test_venue_model(self):
        self.assertEqual(str(self.venue), "Test Venue")

class VenueAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = AppUser.objects.create_user(email='email@email.com',username='testuser',password='test')
        self.client.force_authenticate(user=self.user)
        self.venue_data = {
            "name": "Test Venue",
            "address": "123 Test St",
            "price": 50,
            "status": "Active",
            "contact_name": "John Doe",
            "contact_phone_number": "123-456-7890",
            "event": 1,
        }
        self.venue = Venue.objects.create(**self.venue_data)

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
        updated_data = {"name": "Updated Venue", "address": "123 Test St", "price": 50, "status": "Active", "contact_name": "John Doe", "contact_phone_number": "123-456-7890", "event": 1,}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Updated Venue")

    def test_delete_venue(self):
        url = reverse('venue-retrieve-update-destroy', args=[self.venue.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Venue.objects.filter(id=self.venue.id).exists())

class PhotoModelTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = AppUser.objects.create_user(email='email@email.com',username='testuser',password='test')
        self.client.force_authenticate(user=self.user)
        self.venue = Venue.objects.create(
            name="Test Venue",
            address="123 Test St",
            price=50,
            status="Active",
            contact_name="John Doe",
            contact_phone_number="123-456-7890",
            event=1,
        )
        self.photo = Photo.objects.create(
            venue=self.venue,
            image="https://example.com/path/to/your/image.jpg"
        )

    def test_photo_model(self):
        self.assertEqual(self.photo.venue, self.venue)
        self.assertEqual(str(self.photo), "https://example.com/path/to/your/image.jpg")

class PhotoAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = AppUser.objects.create_user(email='email@email.com',username='testuser',password='test')
        self.client.force_authenticate(user=self.user)
        self.venue = Venue.objects.create(
            name="Test Venue",
            address="123 Test St",
            price=50,
            status="Active",
            contact_name="John Doe",
            contact_phone_number="123-456-7890",
            event=1,
        )
        self.photo_data = {
            "venue": self.venue.id,
            "image": "https://example.com/path/to/your/image.jpg"
        }
        self.photo = Photo.objects.create(venue=self.venue, image=self.photo_data["image"])
        
    def test_create_photo(self):
        url = reverse('photo-create')
        response = self.client.post(url, self.photo_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_get_photo_detail(self):
        url = reverse('photo-retrieve-update-destroy', args=[self.photo.id])
        response = self.client.get(url)
        serializer = PhotoSerializer(self.photo)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_photo(self):
        url = reverse('photo-retrieve-update-destroy', args=[self.photo.id])
        updated_data = {"venue": self.venue.id, "image": "https://example.com/path/to/your/updated/image.jpg"}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['image'], "https://example.com/path/to/your/updated/image.jpg")

    def test_delete_photo(self):
        url = reverse('photo-retrieve-update-destroy', args=[self.photo.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Photo.objects.filter(id=self.photo.id).exists())
