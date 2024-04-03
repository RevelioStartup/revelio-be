from rest_framework import serializers

from task_steps.models import TaskStep 

class TaskStepSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = TaskStep
        fields = '__all__'

    def create(self, validated_data):
        if isinstance(validated_data, list):
            return TaskStep.objects.bulk_create([TaskStep(**item) for item in validated_data])
        return TaskStep.objects.create(**validated_data)