from rest_framework import serializers
from .models import Vendor, PhotoVendor

class PhotoVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoVendor
        fields = '__all__'

class VendorSerializer(serializers.ModelSerializer):
    photos = PhotoVendorSerializer(many=True, read_only=True)

    class Meta:
        model = Vendor
        fields = '__all__'