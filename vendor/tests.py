from django.db import IntegrityError
from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from authentication.models import AppUser
from .models import Vendor, PhotoVendor
from .serializers import VendorSerializer, PhotoVendorSerializer

class BaseTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = AppUser.objects.create_user(email='email@email.com',username='testuser',password='test')
        self.client.force_authenticate(user=self.user)
        self.vendor_data = {
            "name": "Test Vendor",
            "address": "123 Test St",
            "price": 50,
            "status": "PENDING",
            "contact_name": "John Doe",
            "contact_phone_number": "123-456-7890",
            "event": 1,
        }
        self.vendor = Vendor.objects.create(**self.vendor_data)

        self.event_id = 1

        self.vendor1_data = {
            "name": "Vendor 1",
            "address": "123 Test St",
            "price": 50,
            "status": "PENDING",
            "contact_name": "John Doe",
            "contact_phone_number": "123-456-7890",
            "event": self.event_id,
        }
        self.vendor1 = Vendor.objects.create(**self.vendor1_data)

        self.photo = PhotoVendor.objects.create(
            vendor=self.vendor,
            image="https://example.com/path/to/your/image.jpg"
        )

        self.photo_data = {
            "vendor": self.vendor.id,
            "image": "https://example.com/path/to/your/image.jpg"
        }
        self.photo = PhotoVendor.objects.create(vendor=self.vendor, image=self.photo_data["image"])

class VendorModelTestCase(BaseTestCase):
    def test_vendor_model(self):
        self.assertEqual(str(self.vendor), "Test Vendor")

    def test_vendor_does_not_exist(self):
        non_existent_vendor = Vendor.objects.filter(name="Non Existent Vendor").first()
        self.assertIsNone(non_existent_vendor)

class VendorAPITestCase(BaseTestCase):
    def test_get_vendor_list(self):
        url = reverse('vendor-list-create')
        response = self.client.get(url)
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_vendor(self):
        url = reverse('vendor-list-create')
        response = self.client.post(url, self.vendor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_vendor_detail(self):
        url = reverse('vendor-retrieve-update-destroy', args=[self.vendor.id])
        response = self.client.get(url)
        serializer = VendorSerializer(self.vendor)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_vendor(self):
        url = reverse('vendor-retrieve-update-destroy', args=[self.vendor.id])
        updated_data = {"name": "Updated Vendor", "address": "123 Test St", "price": 50, "status": "PENDING", "contact_name": "John Doe", "contact_phone_number": "123-456-7890", "event": 1,}
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


class VendorEventListViewTest(BaseTestCase):
    def test_get_vendors_for_event(self):
        url = reverse('vendor-event-list', kwargs={'event_id': self.event_id})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        expected_data = VendorSerializer([self.vendor, self.vendor1], many=True).data
        self.assertEqual(response.data, expected_data)
    
    def test_get_vendors_for_event_no_vendors(self):
        Vendor.objects.all().delete()
        url = reverse('vendor-event-list', kwargs={'event_id': self.event_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

class PhotoModelTestCase(BaseTestCase):
    def test_photo_model(self):
        self.assertEqual(self.photo.vendor, self.vendor)
        self.assertEqual(str(self.photo), "https://example.com/path/to/your/image.jpg")

    def test_photo_model_no_vendor(self):
        with self.assertRaises(IntegrityError):
            PhotoVendor.objects.create(
                vendor=None,
                image="https://example.com/path/to/your/image.jpg"
            )

    def test_photo_model_no_image(self):
        with self.assertRaises(IntegrityError):
            PhotoVendor.objects.create(
                vendor=self.vendor,
                image=None
            )

class PhotoAPITestCase(BaseTestCase):        
    def test_create_photo(self):
        url = reverse('photo-create')
        response = self.client.post(url, self.photo_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_photo_detail(self):
        url = reverse('photo-retrieve-update-destroy', args=[self.photo.id])
        response = self.client.get(url)
        serializer = PhotoVendorSerializer(self.photo)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_photo(self):
        url = reverse('photo-retrieve-update-destroy', args=[self.photo.id])
        updated_data = {"vendor": self.vendor.id, "image": "https://example.com/path/to/your/updated/image.jpg"}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['image'], "https://example.com/path/to/your/updated/image.jpg")

    def test_delete_photo(self):
        url = reverse('photo-retrieve-update-destroy', args=[self.photo.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(PhotoVendor.objects.filter(id=self.photo.id).exists())

    def test_create_photo_missing_data(self):
        url = reverse('photo-create')
        incomplete_data = {"vendor": self.vendor.id}
        response = self.client.post(url, incomplete_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_photo_detail_does_not_exist(self):
        url = reverse('photo-retrieve-update-destroy', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_photo_does_not_exist(self):
        url = reverse('photo-retrieve-update-destroy', args=[999])
        updated_data = {"vendor": self.vendor.id, "image": "https://example.com/path/to/your/updated/image.jpg"}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_photo_does_not_exist(self):
        url = reverse('photo-retrieve-update-destroy', args=[999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class VendorStatusUpdateAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = AppUser.objects.create_user(email='email@email.com', username='testuser', password='test')
        self.client.force_authenticate(user=self.user)
        self.vendor = Vendor.objects.create(name='Test Vendor', address='Test Address', price=100, status='PENDING',
                                            contact_name='Test Contact', contact_phone_number='123456789', event=1)

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
    
    # test remaining status
    def test_vendor_status_update_to_none(self):
        self._test_status_update('NONE')

    def test_vendor_status_update_to_pending(self):
        self._test_status_update('PENDING')

    def test_vendor_status_update_to_waitlist(self):
        self._test_status_update('WAITLIST')

    def test_vendor_status_update_to_cancelled(self):
        self._test_status_update('CANCELLED')

    def _test_status_update(self, new_status):
        url = reverse('vendor-status-update', kwargs={'pk': self.vendor.pk})
        data = {'status': new_status}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.vendor.refresh_from_db()
        self.assertEqual(self.vendor.status, new_status)
        self.assertEqual(response.data['status'], new_status)