from django.shortcuts import render
from rest_framework import generics

# Create your views here.
class SubscriptionHistory(generics.RetrieveAPIView):
    def get(self, request):
        return render(request, 'subscription/subscription_history.html')