from rest_framework import serializers

from event.models import Event
from venue.serializers import VenueSerializer


class EventSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    venues = VenueSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = '__all__'