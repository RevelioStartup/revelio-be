from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Vendor, PhotoVendor
from .serializers import VendorSerializer, PhotoVendorSerializer, VendorStatusSerializer
from rest_framework.permissions import IsAuthenticated

class VendorListCreateView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    
    def delete(self, request, *args, **kwargs):
        photo = self.get_object()
        photo_pk = photo.pk
        photo.delete()
        return Response({'pk': photo_pk}, status=status.HTTP_204_NO_CONTENT)

class VendorEventListView(APIView):
    def get(self, request, *args, **kwargs):
        event_id = kwargs.get('event_id')
        vendors = Vendor.objects.filter(event=event_id)
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

class PhotoCreateView(generics.CreateAPIView):
    queryset = PhotoVendor.objects.all()
    serializer_class = PhotoVendorSerializer

class PhotoRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PhotoVendor.objects.all()
    serializer_class = PhotoVendorSerializer

    def delete(self, request, *args, **kwargs):
        photo = self.get_object()
        photo_pk = photo.pk
        photo.delete()
        return Response({'pk': photo_pk}, status=status.HTTP_204_NO_CONTENT)

class VendorStatusUpdateAPIView(APIView):
    def patch(self, request, pk):
        try:
            vendor = Vendor.objects.get(pk=pk)
        except Vendor.DoesNotExist:
            return Response({'message': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = VendorStatusSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)