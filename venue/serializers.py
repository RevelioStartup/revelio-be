from rest_framework import serializers
from .models import Venue, Photo

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'

class VenueSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Venue
        fields = '__all__'
