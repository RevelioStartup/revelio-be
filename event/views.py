# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from event.models import Event
from event.serializers import EventSerializer

class EventList(APIView):        
    def get(self, request):
        raise NotImplementedError("This method is not implemented yet!")

class EventDetail(APIView):
    def get_instance(self, id):
        instance = get_object_or_404(Event, pk = id)

        return instance
        
    def get(self, request, id):
        instance = self.get_instance(id)
        serializer = EventSerializer(instance)
        
        return Response(serializer.data)
