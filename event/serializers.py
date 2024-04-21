from rest_framework import serializers

from event.models import Event
from vendor.serializers import VendorSerializer
from venue.serializers import VenueSerializer
from rundown.serializers import RundownSerializer
from rundown.models import Rundown


class EventSerializer(serializers.ModelSerializer):
    rundowns = serializers.SerializerMethodField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    venues = VenueSerializer(many=True, read_only=True)
    vendors = VendorSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = '__all__'
    
    def get_rundowns(self, obj):
        rundowns = Rundown.objects.filter(event_id = obj.id).order_by('rundown_order')

        serializer = RundownSerializer(instance=rundowns, many=True, read_only=True)

        return serializer.data