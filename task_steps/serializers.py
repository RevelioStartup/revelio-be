from rest_framework import serializers

from task_steps.models import TaskStep 

class TaskStepSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = TaskStep
        fields = '__all__'