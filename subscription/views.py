from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response

from subscription.models import Subscription
from subscription.serializers import SubscriptionSerializer

# Create your views here.
class SubscriptionHistory(generics.RetrieveAPIView):
    def get(self, request):
        subscription = Subscription.objects.filter(user=request.user)
        serializer = SubscriptionSerializer(subscription, many=True)
        
        return Response(serializer.data)