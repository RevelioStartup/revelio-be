from rest_framework import serializers

from ai.models import RecommendationHistory


class RecommendationHistorySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = RecommendationHistory
        fields = '__all__'