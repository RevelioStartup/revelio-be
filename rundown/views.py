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

def is_valid_updated_data(rundown: Rundown, new_start_time, new_end_time):
    
    if new_end_time <= new_start_time:
        return False
    
    current_order = rundown.rundown_order
    event_id = rundown.event.id
    prev_rundown = Rundown.objects.all().filter(event_id=event_id, rundown_order=current_order-1)
    next_rundown = Rundown.objects.all().filter(event_id=event_id, rundown_order=current_order+1)
    new_start_time = new_start_time.split(":")
    new_start_time = datetime.time(int(new_start_time[0]), int(new_start_time[1]))
    new_end_time = new_end_time.split(":")
    new_end_time = datetime.time(int(new_end_time[0]), int(new_end_time[1]))
    if len(prev_rundown) > 0:
        prev_rundown = prev_rundown[0]
        prev_end_time = prev_rundown.end_time
        if (prev_end_time > new_start_time): 
            return False
    if len(next_rundown) > 0:
        next_rundown = next_rundown[0]
        next_start_time = next_rundown.start_time
        if (next_start_time < new_end_time): 
            return False
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