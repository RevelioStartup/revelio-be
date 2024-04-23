import os
from midtransclient import CoreApi
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status

class CreatePaymentView(views.APIView):
    def post(self, request):
        # Extract payment data from request data
        order_id = request.data.get('order_id')
        amount = request.data.get('amount')

        # Setup Core API instance
        core_api = CoreApi(
            is_production=os.getenv('MIDTRANS_IS_PRODUCTION') == 'True',
            server_key=os.getenv('MIDTRANS_SERVER_KEY'),
            client_key=os.getenv('MIDTRANS_CLIENT_KEY')
        )

        # Prepare parameter for charge API
        param = {
            "transaction_details": {
                "order_id": order_id,
                "gross_amount": amount
            },
            # TODO: update customer details
             "customer_details": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@midtrans.com",
                "phone": "+62181000000000",
                "notes": "Thank you for your purchase. Please follow the instructions to pay.",
                "customer_details_required_fields": [
                "first_name",
                "phone",
                "email"
                ]
            },
            "callbacks": {
                "finish": "https://yourwebsite.com/finish"
            }
        }

        # Create transaction
        transaction = core_api.charge(param)

        # Check transaction status
        if transaction['transaction_status'] in ['capture', 'settlement']:
            return Response({'message': 'Transaction successful', 'redirect_url': transaction['redirect_url']}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Transaction failed', 'error': transaction}, status=status.HTTP_400_BAD_REQUEST)

