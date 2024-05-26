# Create your views here.
from rest_framework import status
from rest_framework.generics import RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from event.models import Event
from event.serializers import EventSerializer
from utils.permissions import IsOwner, HasEventPlanner, IsPremiumUser
from rest_framework import generics
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
class EventList(APIView): 
    permission_classes = [IsAuthenticated, IsOwner, HasEventPlanner]
           
    def get(self, request):
        events = Event.objects.select_related('user').filter(user = request.user)
        serializer = EventSerializer(events, many=True)
        
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name', 'date', 'location'],  # Update these fields based on your actual Event model
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the event'),
                'date': openapi.Schema(type=openapi.TYPE_STRING, format='date', description='Date of the event'),
                'budget': openapi.Schema(type=openapi.TYPE_NUMBER, description='Budget of the event in Rupiah'),
                'objective': openapi.Schema(type=openapi.TYPE_STRING, description='Objective of the event'),
                'attendees': openapi.Schema(type=openapi.TYPE_NUMBER, description='Number of attendees for the event'),
                'theme': openapi.Schema(type=openapi.TYPE_STRING, description='Theme of the event'),
                'services': openapi.Schema(type=openapi.TYPE_STRING, description='Service of the event'),
                
            },
        ),
        responses={
            201: openapi.Response('Event created successfully', EventSerializer),
            400: 'Bad request',
            403: 'Forbidden - Non-premium users cannot have more than 3 events'
        },
        operation_summary="Register a new event",
        operation_description="Allows users to register a new event. Non-premium users are restricted to a maximum of 3 events."
    )
    def post(self, request):
        user = request.user
        events = Event.objects.filter(user=user)
        event_count = events.count()
    
        is_premium = IsPremiumUser().has_permission(request, view=self)

        if not is_premium and event_count >= 3:
            return Response({"error": "Non-premium users cannot have more than 3 events."}, status=status.HTTP_403_FORBIDDEN)

        serializer = EventSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventDetail(RetrieveDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated, IsOwner, HasEventPlanner]

class EventUpdateView(generics.UpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated, IsOwner, HasEventPlanner]