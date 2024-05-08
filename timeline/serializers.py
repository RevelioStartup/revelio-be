from rest_framework import serializers
from rest_framework.exceptions import NotFound, ValidationError
from .models import Timeline
from task_steps.models import TaskStep
from task_steps.serializers import TaskStepSerializer

class TimelineSerializer(serializers.ModelSerializer):
    task_step = TaskStepSerializer(read_only=True)

    class Meta:
        model = Timeline
        fields = '__all__'

    def validate(self, data):
        if data['end_datetime'] < data['start_datetime']:
            raise ValidationError("End datetime cannot be earlier than start datetime.")
        request = self.context['request']
        task_step_id = request.data.get('task_step')
        existing_timeline = Timeline.objects.filter(task_step_id=task_step_id).exists()
        if existing_timeline:
            raise ValidationError("A timeline with the same task step ID already exists")
        try:
            task_step = TaskStep.objects.get(pk=task_step_id)
            data['task_step'] = task_step
        except TaskStep.DoesNotExist:
            raise NotFound({"error": "Task step not found."})
        
        existing_timelines = Timeline.objects.filter(task_step__task=task_step.task)
        for timeline in existing_timelines:
            if (timeline.task_step.step_order < task_step.step_order and timeline.start_datetime > data['start_datetime']):
                raise ValidationError(
                    "A task step with a larger step order cannot precede a task step with a smaller step order."
                )
            elif timeline.task_step.step_order > task_step.step_order and timeline.start_datetime < data['start_datetime']:
                raise ValidationError(
                    "A task step with a smaller step order cannot follow a task step with a larger step order."
                )

        return data
    def create(self, validated_data):
        return Timeline.objects.create(**validated_data)

class TimelineUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timeline
        fields = ['start_datetime', 'end_datetime']

    def validate(self, data):
        if data['end_datetime'] < data['start_datetime']:
            raise ValidationError("End datetime cannot be earlier than start datetime.")
        
        existing_timelines = Timeline.objects.filter(task_step__task=self.instance.task_step.task)
        
        for timeline in existing_timelines:
            if (timeline.task_step.step_order < self.instance.task_step.step_order and timeline.start_datetime > data['start_datetime']):
                raise ValidationError(
                    "A task step with a larger step order cannot precede a task step with a smaller step order."
                )
            elif timeline.task_step.step_order > self.instance.task_step.step_order and timeline.start_datetime < data['start_datetime']:
                raise ValidationError(
                    "A task step with a smaller step order cannot follow a task step with a larger step order."
                )
        return data