import os
import uuid
from midtransclient import Snap
from rest_framework import views, status, generics
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.db import transaction as db_transaction
from .models import Transaction
from package.models import Package
from subscription.models import Subscription
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from .serializers import TransactionSerializer
from django.utils import timezone
from utils.permissions import IsOwner
from rest_framework.exceptions import PermissionDenied

SNAP_API = Snap(
    is_production=os.getenv('MIDTRANS_IS_PRODUCTION') == 'True',
    server_key=os.getenv('MIDTRANS_SERVER_KEY'),
)

class CreatePaymentView(views.APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'package_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
            required=['package_id'],
        ),
        responses={
            200: 'Payment created successfully',
            400: 'Bad request'
        },
        operation_summary="Create Payment",
    )
    def post(self, request):
        user = request.user
        package_id = request.data.get('package_id')
        chosen_package = get_object_or_404(Package, id=package_id)
        order_id = str(uuid.uuid4())
        order_amount = chosen_package.price

        param = {
            "transaction_details": {
                "order_id": order_id,
                "gross_amount": order_amount
            },
            "customer_details": {
                "first_name": user.username,
                "email": user.email,
                "notes": "Thank you for your subscription. Please follow the instructions to pay.",
                "customer_details_required_fields": [
                    "email"
                ]
            },
            "callbacks": {
                "finish": str(os.getenv('REVELIO_FE_BASE_URL'))+'/payment'
            }
        }
        try:
            with db_transaction.atomic():
                transaction = SNAP_API.create_transaction(param)
                Transaction.objects.create(
                    order_id=order_id,
                    price=order_amount,
                    user=user,
                    package=chosen_package,
                    midtrans_url=transaction['redirect_url']
                )

                return Response({'message': 'Transaction successful', 'redirect_url': transaction['redirect_url']}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'message': 'Transaction failed'}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="order_id",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=True,
                description="Order ID",
            ),
        ],
        responses={
            200: 'Transaction successful',
            400: 'Bad request'
        },
        operation_summary="Get Payment Details",
    )
    
    def get(self, request):
        order_id = request.query_params.get('order_id')
        user = request.user

        if not order_id:
            return Response({"error": "Order ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with db_transaction.atomic():
                midtrans_transaction = SNAP_API.transactions.status(order_id)

                payment_status = midtrans_transaction.get("transaction_status")
                transaction_object = get_object_or_404(Transaction, order_id=order_id)
                if transaction_object.status != payment_status:
                    transaction_object.status = payment_status
                    if(transaction_object.status=='expire'):
                        transaction_object.midtrans_url=None

                    if(payment_status=="settlement"):
                        transaction_object.midtrans_url=None
                        start_subscription = timezone.now()
                        duration_days = transaction_object.package.duration
                        end_subscription = start_subscription + timedelta(days=duration_days)
                        Subscription.objects.create(
                            user=user,
                            start_date=start_subscription,
                            end_date=end_subscription,
                            plan=transaction_object.package
                        )

                if not transaction_object.payment_type:
                    transaction_object.payment_type = midtrans_transaction.get("payment_type")
                    transaction_object.payment_merchant = midtrans_transaction.get("acquirer")
                    transaction_object.checkout_time = datetime.strptime(midtrans_transaction.get("transaction_time"), "%Y-%m-%d %H:%M:%S")
                    transaction_object.expiry_time = datetime.strptime(midtrans_transaction.get("expiry_time"), "%Y-%m-%d %H:%M:%S")
                    transaction_object.midtrans_transaction_id = midtrans_transaction.get("transaction_id")

                transaction_object.save()

                return Response({'message': midtrans_transaction.get("status_message"), 'transaction_detail': TransactionSerializer(transaction_object).data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
class TransactionListAPIView(generics.ListAPIView):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)
    
   
class TransactionDetailAPIView(generics.RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    lookup_field='id'

    def get_object(self):
        obj = super().get_object()
        if not IsOwner().has_object_permission(self.request, self, obj):
            raise PermissionDenied("You do not have permission to view this transaction")
        return obj
