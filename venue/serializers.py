import uuid
from rest_framework import serializers
from .models import Venue, PhotoVenue

class PhotoVenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoVenue
        fields = '__all__'

class VenueSerializer(serializers.ModelSerializer):
    photos = PhotoVenueSerializer(many=True, read_only=True)

    class Meta:
        model = Venue
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        for field in ret:
            if isinstance(ret[field], uuid.UUID):
                ret[field] = str(ret[field])
        return ret

class VenueStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ['status']