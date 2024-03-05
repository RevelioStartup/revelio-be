from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Vendor, PhotoVendor
from .serializers import VendorSerializer, PhotoVendorSerializer
from rest_framework.permissions import IsAuthenticated

class VendorListCreateView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

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