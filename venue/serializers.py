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

class VenueStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ['status']