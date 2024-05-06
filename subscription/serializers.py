from rest_framework import serializers

from package.serializers import PackageSerializer
from subscription.models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'user', 'plan', 'start_date', 'end_date', 'is_active']
        
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['plan'] = PackageSerializer(instance.plan).data
        
        return response
        