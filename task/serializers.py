import uuid
from rest_framework import serializers

from task_steps.serializers import TaskStepSerializer
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    task_steps = TaskStepSerializer(many=True, read_only=True)
    
    class Meta:
        model = Task
        fields = '__all__'
