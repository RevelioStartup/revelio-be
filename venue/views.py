from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Venue, PhotoVenue
from .serializers import VenueSerializer, PhotoVenueSerializer, VenueStatusSerializer

class VenueListCreateView(generics.ListCreateAPIView):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer

class VenueRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer

    def delete(self, request, *args, **kwargs):
        venue = self.get_object()
        venue_pk = venue.pk
        venue.delete()
        return Response({'pk': venue_pk}, status=status.HTTP_204_NO_CONTENT)

class VenueEventListView(APIView):
    def get(self, request, *args, **kwargs):
        event_id = kwargs.get('event_id')
        venues = Venue.objects.filter(event=event_id)
        serializer = VenueSerializer(venues, many=True)
        return Response(serializer.data)

class PhotoCreateView(generics.CreateAPIView):
    queryset = PhotoVenue.objects.all()
    serializer_class = PhotoVenueSerializer

class PhotoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PhotoVenue.objects.all()
    serializer_class = PhotoVenueSerializer

    def delete(self, request, *args, **kwargs):
        photo = self.get_object()
        photo_pk = photo.pk
        photo.delete()
        return Response({'pk': photo_pk}, status=status.HTTP_204_NO_CONTENT)

class VenueStatusUpdateAPIView(APIView):
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