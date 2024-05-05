import os
from unittest.mock import patch
from rest_framework import status
from django.urls import reverse
from .models import Transaction
from authentication.models import AppUser
from rest_framework.test import APIClient, APITestCase

SNAP_API = 'payment.views.SNAP_API'

class CreatePaymentViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = AppUser.objects.create_user(email='user@example.com', username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

        self.url = reverse('payment:create-payment') 

    @patch(SNAP_API)
    def test_create_payment_success(self, mock_snap_api):
        mock_snap_api.create_transaction.return_value = {
            'token': 'dummy_token',
            'redirect_url': 'http://dummy_redirect_url.com'
        }

        data = {'order_id': 'test_order', 'amount': 100}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('redirect_url', response.data)

        self.assertEqual(Transaction.objects.count(), 1)
        self.assertTrue(Transaction.objects.filter(order_id='test_order').exists())

    @patch(SNAP_API)
    def test_get_payment_details(self, mock_snap_api):
        mock_snap_api.transactions.status.return_value = {
            'payment_type': 'dummy_payment_type',
            'acquirer': 'dummy_acquirer',
            'transaction_time': '2024-04-30 00:27:59',
            'expiry_time': '2024-04-30 00:42:59',
            'transaction_status': 'dummy_transaction_status',
            'transaction_id': 'dummy_transaction_id',
            'status_message': 'dummy_status_message'
        }

        transaction = Transaction.objects.create(order_id='test_order',price=100 ,user=self.user)

        response = self.client.get(f"{self.url}?order_id=test_order")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('transaction_detail', response.data)
    
    def test_missing_order_id_parameter(self):
        response = self.client.get(self.url) 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch(SNAP_API)
    def test_get_payment_details_failure(self, mock_snap_api):
        mock_snap_api.transactions.status.return_value = None
        response = self.client.get(f"{self.url}?order_id=test_order")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


