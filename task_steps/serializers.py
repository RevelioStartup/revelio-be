from rest_framework import serializers
from task_steps.models import TaskStep 

class TaskStepSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    start_datetime = serializers.SerializerMethodField()
    end_datetime = serializers.SerializerMethodField()

    class Meta:
        model = TaskStep
        fields = '__all__'
    
    def get_start_datetime(self, obj):
        timeline = obj.timelines.first() 
        if timeline:
            return timeline.start_datetime
        return None
    
    def get_end_datetime(self, obj):
        timeline = obj.timelines.first()  
        if timeline:
            return timeline.end_datetime
        return None

    def create(self, validated_data):
        if isinstance(validated_data, list):
            return TaskStep.objects.bulk_create([TaskStep(**item) for item in validated_data])
        return TaskStep.objects.create(**validated_data)
