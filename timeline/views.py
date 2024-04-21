from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status, serializers
from rest_framework.response import Response
from .serializers import TimelineSerializer
from .models import Timeline
from task_steps.models import TaskStep
from drf_yasg import openapi

class TimelineCreateView(generics.CreateAPIView):
    queryset = Timeline.objects.all()
    serializer_class = TimelineSerializer

    @swagger_auto_schema(
        operation_summary="Create a new timeline",
        operation_description="Create a new timeline with start and end datetimes and a specific task step.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['task_step', 'start_datetime', 'end_datetime'],
            properties={
                'task_step': openapi.Schema(type=openapi.TYPE_STRING, description="UUID of the Task Step"),
                'start_datetime': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description="Start date and time of the timeline"),
                'end_datetime': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description="End date and time of the timeline"),
            }
        ),
        responses={
            201: TimelineSerializer(),
            400: 'Bad request - Data validation error or missing data',
            404: 'Not found - Task step does not exist'
        }
    )
    def post(self, request, *args, **kwargs):
        task_step_id = request.data.get('task_step')
        if not task_step_id:
            return Response({"error": "Task step ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            task_step = TaskStep.objects.get(pk=task_step_id)
        except TaskStep.DoesNotExist:
            return Response({"error": "Task step does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        existing_timeline = Timeline.objects.filter(task_step_id=task_step_id).exists()
        if existing_timeline:
            return Response({"error": "A timeline with the same task step ID already exists"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save(task_step=task_step)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)