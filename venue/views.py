from django.shortcuts import render

# Create your views here.

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Venue, Photo
from .serializers import VenueSerializer, PhotoSerializer


class VenueListCreateView(generics.ListCreateAPIView):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer

class VenueRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer

class VenueEventListView(APIView):
    def get(self, request, *args, **kwargs):
        event_id = kwargs.get('event_id')
        venues = Venue.objects.filter(event=event_id)
        serializer = VenueSerializer(venues, many=True)
        return Response(serializer.data)

class PhotoCreateView(generics.CreateAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

class PhotoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
