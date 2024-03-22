from rest_framework import serializers

from task_steps.models import TaskStep 

class TaskStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStep
        fields = '__all__'