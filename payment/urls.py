from django.urls import path
from .views import CreatePaymentView

app_name = 'payment'

urlpatterns = [
    path('create/', CreatePaymentView.as_view(), name='create-payment'),
]
