import uuid
from unittest.mock import patch
from rest_framework import status
from django.urls import reverse
from .models import Transaction
from authentication.models import AppUser
from rest_framework.test import APIClient
from package.models import Package
from utils.base_test import BaseTestCase
from django.contrib.auth.models import BaseUserManager

SNAP_API = 'payment.views.SNAP_API'

class CreatePaymentViewTestCase(BaseTestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.another_user)
        self.url = reverse('payment:create-payment')
        self.package = Package.objects.create(
            name="Dummy Premium",
            price=10000,
            duration=30,
            event_planner=True,
            event_tracker=True,
            event_timeline=True,
            event_rundown=True,
            ai_assistant=True
        )

    @patch(SNAP_API)
    def test_create_payment_success(self, mock_snap_api):
        mock_snap_api.create_transaction.return_value = {
            'token': 'dummy_token',
            'redirect_url': 'http://dummy_redirect_url.com'
        }

        data = {'package_id': self.package.pk, 'order_id': str(uuid.uuid4())}  
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('redirect_url', response.data)

        self.assertEqual(Transaction.objects.count(), 1)
        self.assertTrue(Transaction.objects.filter(user=self.another_user).exists())

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

        transaction = Transaction.objects.create(order_id=str(uuid.uuid4()), price=100, user=self.another_user, package=self.package)

        response = self.client.get(f"{self.url}?order_id={transaction.order_id}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('transaction_detail', response.data)

    def test_missing_order_id_parameter(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch(SNAP_API)
    def test_get_payment_details_failure(self, mock_snap_api):
        mock_snap_api.transactions.status.return_value = None
        # Create a transaction with a UUID order_id
        transaction = Transaction.objects.create(order_id=str(uuid.uuid4()), price=100, user=self.another_user, package=self.package)
        response = self.client.get(f"{self.url}?order_id={transaction.order_id}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TransactionListAPIViewTestCase(BaseTestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.another_user)
        self.url = reverse('payment:transaction-list')
        self.package = Package.objects.create(
            name="Dummy Premium",
            price=10000,
            duration=30,
            event_planner=True,
            event_tracker=True,
            event_timeline=True,
            event_rundown=True,
            ai_assistant=True
        )
        self.transaction = Transaction.objects.create(order_id=str(uuid.uuid4()), price=100, user=self.another_user, package=self.package)

    def test_get_transaction_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        transactions = response.data
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0]['order_id'], str(self.transaction.order_id))
        self.assertEqual(transactions[0]['price'], self.transaction.price)

    def test_get_transaction_list_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class TransactionDetailAPIViewTestCase(BaseTestCase):
    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.another_user)
        self.package = Package.objects.create(
            name="Dummy Premium",
            price=10000,
            duration=30,
            event_planner=True,
            event_tracker=True,
            event_timeline=True,
            event_rundown=True,
            ai_assistant=True
        )
        self.order_id = str(uuid.uuid4())
        self.transaction = Transaction.objects.create(order_id=self.order_id, price=100, user=self.another_user, package=self.package)

    def test_get_transaction_detail(self):
        url = reverse('payment:transaction-detail', kwargs={'id': self.transaction.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        transaction_data = response.data
        self.assertEqual(transaction_data.get('order_id'), self.transaction.order_id)
        self.assertEqual(transaction_data.get('price'), self.transaction.price)
        self.assertEqual(transaction_data.get('midtrans_transaction_id'), self.transaction.midtrans_transaction_id)

    def test_get_transaction_detail_unauthorized(self):
        url = reverse('payment:transaction-detail', kwargs={'id': self.transaction.id})
        other_password = BaseUserManager().make_random_password()
        other_user = AppUser.objects.create_user(email='otheruser@example.com', username='otheruser', password=other_password)
        self.client.force_authenticate(user=other_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_transaction_detail_nonexistent_id(self):
        nonexistent_id = uuid.uuid4()
        url = reverse('payment:transaction-detail', kwargs={'id': nonexistent_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
