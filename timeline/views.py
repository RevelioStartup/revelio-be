from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status, serializers
from rest_framework.response import Response

from event.models import Event
from .serializers import TimelineSerializer, TimelineUpdateSerializer
from .models import Timeline
from drf_yasg import openapi
from revelio.utils import get_validation_error_detail
from utils.permissions import IsEventOwner
from rest_framework.permissions import IsAuthenticated

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
        
class TimelineDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Timeline.objects.all()
    serializer_class = TimelineSerializer

    @swagger_auto_schema(
        operation_summary="Update a timeline",
        operation_description="Update a timeline by its UUID.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'start_datetime': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description="Start date and time of the timeline"),
                'end_datetime': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description="End date and time of the timeline"),
            }
        ),
        responses={
            200: TimelineSerializer(),
            400: 'Bad request - Data validation error or missing data',
            404: 'Not found - Timeline does not exist'
        }
    )
    
    def patch(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = TimelineUpdateSerializer(instance, data=request.data, partial=True)
            
            if(serializer.is_valid()):
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except serializers.ValidationError as e:
            error_message = get_validation_error_detail(e)
            return Response({"error": error_message}, status=status.HTTP_404_NOT_FOUND)
        
    def get_object(self):
        try:
            return Timeline.objects.get(pk=self.kwargs['pk'])
        except Timeline.DoesNotExist:
            raise serializers.ValidationError("Timeline does not exist")
        
class TimelineDeleteView(generics.DestroyAPIView):
    queryset = Timeline.objects.all()
    serializer_class = TimelineSerializer
    lookup_field = 'id'  

    def delete(self, request, *args, **kwargs):
        timeline = self.get_object()
        timeline.delete()
        return Response({"message": "Timeline deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class TimelineList(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsEventOwner]
    serializer_class = TimelineSerializer

    def get_queryset(self):
        event_id = self.kwargs.get('event_id')
        if not Event.objects.filter(id=event_id).exists():
            raise Http404("No Event matches the given query.")
        return Timeline.objects.filter(task_step__task__event_id=event_id)
    

