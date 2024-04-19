from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from event.models import Event
from .models import Rundown
from .serializers import RundownSerializer
from rest_framework.response import Response
import datetime

def validate_rundown_data(rundown_data):
    prev_end_time = datetime.time(0,0)
    for data in rundown_data:
        start_time = data["start_time"].split(":")
        start_time = datetime.time(int(start_time[0]), int(start_time[1]))
        end_time = data["end_time"].split(":")
        end_time = datetime.time(int(end_time[0]), int(end_time[1]))
        if start_time < prev_end_time or start_time >= end_time:
            return False
        prev_end_time = end_time
    return True


class RundownCreateView(APIView):
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
    
class RundownUpdateView(APIView):
    def patch(self, request, id):
        pass