from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Venue, Photo
from .serializers import VenueSerializer, PhotoSerializer, VenueStatusSerializer
from rest_framework.permissions import IsAuthenticated

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

class VenueStatusUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request, pk):
        try:
            venue = Venue.objects.get(pk=pk)
        except Venue.DoesNotExist:
            return Response({'message': 'Venue not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = VenueStatusSerializer(venue, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)