import uuid
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
        
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        for field in ret:
            if isinstance(ret[field], uuid.UUID):
                ret[field] = str(ret[field])
        return ret

class VendorStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['status']