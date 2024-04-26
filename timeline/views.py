from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status, serializers
from rest_framework.response import Response
from .serializers import TimelineSerializer
from .models import Timeline
from task_steps.models import TaskStep
from drf_yasg import openapi
from revelio.utils import get_validation_error_detail

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
    def get_serializer_context(self):
        return {'request': self.request}
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            error_message = get_validation_error_detail(e)
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
        
class TimelineDeleteView(generics.DestroyAPIView):
    queryset = Timeline.objects.all()
    serializer_class = TimelineSerializer
    lookup_field = 'id'  

    def delete(self, request, *args, **kwargs):
        timeline = self.get_object()
        timeline.delete()
        return Response({"message": "Timeline deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


    
