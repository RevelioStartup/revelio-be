from django.shortcuts import render
from rest_framework import generics

# Create your views here.
class SubscriptionHistory(generics.RetrieveAPIView):
    def get(self, request):
        return NotImplementedError("This view is not implemented yet")