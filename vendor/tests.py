from datetime import date
from decimal import Decimal
import json
from uuid import UUID
import uuid
from django.db import IntegrityError
from django.forms import ValidationError
from django.test import TestCase
from collections import OrderedDict

# Create your tests here.

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from authentication.models import AppUser
from .models import Vendor, PhotoVendor, Event
from .serializers import VendorSerializer
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.serializers.json import DjangoJSONEncoder

class BaseTestCaseVendor(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = AppUser.objects.create_user(email='email@email.com',username='testuser',password='test')
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
        self.vendor_data = {
            "name": "Test Vendor",
            "address": "123 Test St",
            "price": 50,
            "status": "PENDING",
            "contact_name": "John Doe",
            "contact_phone_number": "123-456-7890",
            "event_id": self.event_id,
        }
        self.vendor = Vendor.objects.create(**self.vendor_data)

        self.vendor1_data = {
            "name": "Vendor 1",
            "address": "123 Test St",
            "price": 50,
            "status": "PENDING",
            "contact_name": "John Doe",
            "contact_phone_number": "123-456-7890",
            "event_id": self.event_id,
        }
        self.vendor1 = Vendor.objects.create(**self.vendor1_data)

        self.vendor2_data = {
            "name": "Vendor 2",
            "address": "456 Test St",
            "price": 60,
            "status": "NONE",
            "contact_name": "Jane Doe",
            "contact_phone_number": "987-654-3210",
            "event_id": "9fdfb487-5101-4824-8c3b-0775732aacda",
        }
        self.vendor2 = Vendor.objects.create(**self.vendor2_data)

class BaseTestCasePhoto(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = AppUser.objects.create_user(email='email@email.com',username='testuser',password='test')
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
        
        self.vendor_data = {
            "name": "Test Vendor",
            "address": "123 Test St",
            "price": 50,
            "status": "PENDING",
            "contact_name": "John Doe",
            "contact_phone_number": "1234567890",
            "event_id": "9fdfb487-5101-4824-8c3b-0775732aacda",
        }
        self.vendor = Vendor.objects.create(**self.vendor_data)

        with open('empathymap.jpg', 'rb') as img:
            self.photo = PhotoVendor.objects.create(
                vendor=self.vendor,
                image=SimpleUploadedFile(img.name, img.read())
            )
            
        with open('empathymap.jpg', 'rb') as img:
            img_content = img.read()
            self.photo_data = {
                "vendor": self.vendor,
                "image": SimpleUploadedFile(img.name, img_content)
            }
            self.photo = PhotoVendor.objects.create(**self.photo_data)

class VendorModelTestCase(BaseTestCaseVendor):
    def test_vendor_model(self):
        self.assertEqual(str(self.vendor), "Test Vendor")

    def test_vendor_does_not_exist(self):
        non_existent_vendor = Vendor.objects.filter(name="Non Existent Vendor").first()
        self.assertIsNone(non_existent_vendor)

class VendorAPITestCase(BaseTestCaseVendor):
    def test_get_vendor_list(self):
        url = reverse('vendor-list-create')
        response = self.client.get(url)
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_vendor(self):
        new_data = {"name": "Updated Vendor", "address": "123 Test St", "price": 50, "status": "PENDING", "contact_name": "John Doe", "contact_phone_number": "123-456-7890", "event": self.event_id}
        url = reverse('vendor-list-create')
        response = self.client.post(url, new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_vendor_detail(self):
        url = reverse('vendor-retrieve-update-destroy', args=[self.vendor.id])
        response = self.client.get(url)
        serializer = VendorSerializer(self.vendor)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_vendor(self):
        url = reverse('vendor-retrieve-update-destroy', args=[self.vendor.id])
        updated_data = {"name": "Updated Vendor", "address": "123 Test St", "price": 50, "status": "PENDING", "contact_name": "John Doe", "contact_phone_number": "123-456-7890", "event": self.event_id}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Updated Vendor")

    def test_delete_vendor(self):
        url = reverse('vendor-retrieve-update-destroy', args=[self.vendor.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Vendor.objects.filter(id=self.vendor.id).exists())

    def test_get_vendor_list_no_vendors(self):
        Vendor.objects.all().delete()
        url = reverse('vendor-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_create_vendor_missing_data(self):
        url = reverse('vendor-list-create')
        incomplete_data = {"name": "Incomplete Vendor"}
        response = self.client.post(url, incomplete_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_vendor_detail_does_not_exist(self):
        url = reverse('vendor-retrieve-update-destroy', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_vendor_does_not_exist(self):
        url = reverse('vendor-retrieve-update-destroy', args=[999])
        updated_data = {"name": "Updated Vendor"}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_vendor_does_not_exist(self):
        url = reverse('vendor-retrieve-update-destroy', args=[999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class VendorEventListViewTest(BaseTestCaseVendor):
    def test_get_vendors_for_event(self):
        url = reverse('vendor-event-list', kwargs={'event_id': "9fdfb487-5101-4824-8c3b-0775732aacda"})
        response = self.client.get(url)
        response_data = json.loads(json.dumps(response.data), object_pairs_hook=OrderedDict)
        expected_data = VendorSerializer([self.vendor, self.vendor1, self.vendor2], many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, expected_data)
    
    def test_get_vendors_for_event_no_vendors(self):
        Vendor.objects.all().delete()
        url = reverse('vendor-event-list', kwargs={'event_id': "9fdfb487-5101-4824-8c3b-0775732aacda"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

class PhotoModelTestCase(BaseTestCasePhoto):
    def test_photo_model(self):
        self.assertTrue(str(self.photo).startswith('https://storage.googleapis.com/bucket-revelio-1'))

    def test_photo_model_no_vendor(self):
        with self.assertRaises(IntegrityError):
            PhotoVendor.objects.create(
                vendor=None,
                image=SimpleUploadedFile(name='empathymap.jpg', content=open('empathymap.jpg', 'rb').read())
            )

    def test_photo_model_no_image(self):
        with self.assertRaises(ValidationError):
            photo = PhotoVendor(vendor=self.vendor)
            photo.full_clean()

class PhotoAPITestCase(BaseTestCasePhoto):        
    def test_create_photo(self):
        url = reverse('photo-vendor-create')
        self.photo_data['vendor'] = self.vendor.id
        with open('empathymap.jpg', 'rb') as img:
            self.photo_data['image'] = SimpleUploadedFile(img.name, img.read())
            response = self.client.post(url, self.photo_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_photo_detail(self):
        url = reverse('photo-vendor-retrieve-update-destroy', args=[self.photo.id])
        response = self.client.get(url)
        self.assertTrue(self.photo.image.url.startswith('https://storage.googleapis.com/bucket-revelio-1'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_photo(self):
        url = reverse('photo-vendor-retrieve-update-destroy', args=[self.photo.id])
        with open('empathymap.jpg', 'rb') as img:
            updated_data = {"vendor": self.vendor.id, "image": SimpleUploadedFile(img.name, img.read())}
            response = self.client.put(url, updated_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.photo.image.url.startswith('https://storage.googleapis.com/bucket-revelio-1'))

    def test_create_photo_missing_data(self):
        url = reverse('photo-vendor-create')
        incomplete_data = {"vendor": self.vendor.id}
        response = self.client.post(url, incomplete_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_photo_detail_does_not_exist(self):
        url = reverse('photo-vendor-retrieve-update-destroy', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_photo_does_not_exist(self):
        url = reverse('photo-vendor-retrieve-update-destroy', args=[999])
        with open('empathymap.jpg', 'rb') as img:
            updated_data = {"vendor": self.vendor.id, "image": SimpleUploadedFile(img.name, img.read())}
            response = self.client.put(url, updated_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_photo(self):
        url = reverse('photo-vendor-retrieve-update-destroy', args=[self.photo.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, {'pk': self.photo.pk})

    def test_delete_photo_does_not_exist(self):
        url = reverse('photo-vendor-retrieve-update-destroy', args=[999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class VendorStatusUpdateAPITest(BaseTestCaseVendor):
    def test_vendor_status_update(self):
        url = reverse('vendor-status-update', kwargs={'pk': self.vendor.pk})
        data = {'status': 'CONFIRMED'}  
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'CONFIRMED')

    def test_vendor_status_update_invalid_vendor_id(self):
        url = reverse('vendor-status-update', kwargs={'pk': 999})  
        data = {'status': 'CONFIRMED'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_vendor_status_update_invalid_status(self):
        url = reverse('vendor-status-update', kwargs={'pk': self.vendor.pk})
        data = {'status': 'INVALID_STATUS'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

