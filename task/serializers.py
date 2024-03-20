import uuid
from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    # TODO: Uncomment to set task as a foreign key of step
    # steps = StepSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = '__all__'
