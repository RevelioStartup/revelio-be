import os
from midtransclient import Snap
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db import transaction as db_transaction
from .models import Transaction
from django.shortcuts import get_object_or_404
from authentication.models import AppUser
from datetime import datetime
from .serializers import TransactionSerializer

SNAP_API = Snap(
    is_production=os.getenv('MIDTRANS_IS_PRODUCTION') == 'True',
    server_key=os.getenv('MIDTRANS_SERVER_KEY'),
)

class CreatePaymentView(views.APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'order_id': openapi.Schema(type=openapi.TYPE_STRING),
                'amount': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
            required=['order_id', 'amount'],
        ),
        responses={
            200: 'Payment created successfully',
            400: 'Bad request'
        },
        operation_summary="Create Payment",
    )
    def post(self, request):
        user = request.user
        order_id = request.data.get('order_id')
        amount = request.data.get('amount')

        param = {
            "transaction_details": {
                "order_id": order_id,
                "gross_amount": amount
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
                "finish": str(os.getenv('REVELIO_FE_BASE_URL'))+'payment/success/'
            }
        }
        try:
            with db_transaction.atomic():
                transaction = SNAP_API.create_transaction(param)
                Transaction.objects.create(
                    order_id=order_id,
                    price=amount,
                    midtrans_token=transaction['token'],
                    user=AppUser.objects.get(pk=user.id)
                )

                return Response({'message': 'Transaction successful', 'redirect_url': transaction['redirect_url']}, status=status.HTTP_200_OK)

        except Exception as e:
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

        if not order_id:
            return Response({"error": "Order ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with db_transaction.atomic():
                midtrans_transaction = SNAP_API.transactions.status(order_id)

                transaction_object = get_object_or_404(Transaction, order_id=order_id)
                if not transaction_object.payment_type:
                    transaction_object.payment_type = midtrans_transaction.get("payment_type")
                    transaction_object.payment_merchant = midtrans_transaction.get("acquirer")
                    transaction_object.checkout_time = datetime.strptime(midtrans_transaction.get("transaction_time"), "%Y-%m-%d %H:%M:%S")
                    transaction_object.expiry_time = datetime.strptime(midtrans_transaction.get("expiry_time"), "%Y-%m-%d %H:%M:%S")
                    transaction_object.status = midtrans_transaction.get("transaction_status")
                    transaction_object.midtrans_transaction_id = midtrans_transaction.get("transaction_id")

                    transaction_object.save()

                return Response({'message': midtrans_transaction.get("status_message"), 'transaction_detail': TransactionSerializer(transaction_object).data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
