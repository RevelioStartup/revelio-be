from rest_framework import serializers

from .models import Timeline
from task_steps.serializers import TaskStepSerializer

class TimelineSerializer(serializers.ModelSerializer):
    task_step = TaskStepSerializer(read_only=True)

    class Meta:
        model = Timeline
        fields = '__all__'

    def validate(self, data):
        if data['end_datetime'] < data['start_datetime']:
            raise serializers.ValidationError("End datetime cannot be earlier than start datetime.")

        return data

    