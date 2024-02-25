# Create your views here.
from rest_framework import status
from rest_framework.generics import RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from event.models import Event
from event.serializers import EventSerializer
from utils.permissions import IsOwner

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

class EventDetail(RetrieveDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated, IsOwner]