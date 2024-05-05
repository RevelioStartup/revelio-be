from rest_framework import serializers

from subscription.models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['user', 'plan', 'start_date', 'end_date', 'is_active']
        