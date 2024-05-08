from django.urls import path
from .views import CreatePaymentView, TransactionListAPIView, TransactionDetailAPIView

app_name = 'payment'

urlpatterns = [
    path('create/', CreatePaymentView.as_view(), name='create-payment'),
    path('transactions/', TransactionListAPIView.as_view(), name='transaction-list'),
    path('transactions/<uuid:id>/', TransactionDetailAPIView.as_view(), name='transaction-detail'),
]
