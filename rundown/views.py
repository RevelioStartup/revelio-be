from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from event.models import Event
from .models import Rundown
from .serializers import RundownSerializer
from rest_framework.response import Response
from .validators import validate_rundown_data, is_valid_updated_data
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class RundownCreateView(APIView):

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['event_id', 'rundown_data'],
            properties={
                'event_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Event ID'),
                'rundown_data': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    description='List of rundowns',
                    items=openapi.Items(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'description': openapi.Schema(type=openapi.TYPE_STRING, description='Activity that time in rundown'),
                            'start_time': openapi.Schema(type=openapi.TYPE_STRING, description='Start time of the activity'),
                            'end_time': openapi.Schema(type=openapi.TYPE_STRING, description='End time of the activity'),
                        }
                    )
                ),
            },
        ),
        responses={201: RundownSerializer(many=True), 400: 'Bad Request', 500: 'Internal Server Error'}
    )
    def post(self, request):
        event_id = request.data.get('event_id')
        rundown_data = request.data.get('rundown_data')

        event = get_object_or_404(Event, id=event_id)

        if Rundown.objects.filter(event=event).exists():
            return Response({"error": "Rundown for that event already exists"}, status=400)

        if not validate_rundown_data(rundown_data):
            return Response({"error": "Invalid rundown data"}, status=400)
        
        order = 1

        for data in rundown_data:
            data["event_id"] = event_id
            data["rundown_order"] = order
            order += 1
        
        created_rundown = Rundown.objects.bulk_create([Rundown(**data) for data in rundown_data])
        rundown_serializers = RundownSerializer(created_rundown, many=True)
        return Response(rundown_serializers.data, status=201)    
    
class RundownDetailView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['description', 'start_time, end_time'],
            properties={
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='Activity that time in rundown'),
                'start_time': openapi.Schema(type=openapi.TYPE_STRING, description='Start time of the activity'),
                'end_time': openapi.Schema(type=openapi.TYPE_STRING, description='End time of the activity'),
            },
        ),
        responses={200: RundownSerializer(), 400: 'Bad Request', 500: 'Internal Server Error'}
    )
    def patch(self, request, id):
        new_start_time = request.data.get("start_time")
        new_end_time = request.data.get("end_time")
        new_description = request.data.get("description")

        updated_rundown = get_object_or_404(Rundown, id = id)

        if not is_valid_updated_data(updated_rundown, new_start_time, new_end_time):
            return Response({"message":"Invalid rundown data"}, status=400)
        
        updated_rundown.start_time = new_start_time
        updated_rundown.end_time = new_end_time
        updated_rundown.description = new_description
        updated_rundown.save()
        rundown_serializers = RundownSerializer(updated_rundown)
        return Response(rundown_serializers.data, status=200) 