import uuid
from rest_framework import serializers

from task_steps.serializers import TaskStepSerializer
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    task_steps = serializers.SerializerMethodField()
    
    class Meta:
        model = Task
        fields = '__all__'

    def get_task_steps(self, obj):
        task_steps = obj.task_steps.all().order_by('step_order')
        serializer = TaskStepSerializer(instance=task_steps, many=True, read_only=True)

        return serializer.data
