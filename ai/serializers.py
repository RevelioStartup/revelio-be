from rest_framework import serializers

from ai.models import AIRecommendation


class RecommendationSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = AIRecommendation
        fields = '__all__'