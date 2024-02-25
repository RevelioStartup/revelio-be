# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from event.models import Event
from event.serializers import EventSerializer

class EventList(APIView):        
    def get(self, request):
        events = Event.objects.select_related('user').filter(user = request.user)
        serializer = EventSerializer(events, many=True)
        
        return Response(serializer.data)

    def post(self, request):
        serializer = EventSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventDetail(APIView):
    def get_instance(self, id):
        instance = get_object_or_404(Event, pk = id)

        return instance
        
    def get(self, request, id):
        instance = self.get_instance(id)
        serializer = EventSerializer(instance)
        
        return Response(serializer.data)
    
    def delete(self, request, id):
        raise NotImplementedError()