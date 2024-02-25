# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from event.models import Event

class EventList(APIView):        
    def get(self, request, id):
        return Response()     

class EventDetail(APIView):
    def get_instance(self, id):
        instance = Event.objects.get_object_or_404(pk = id)

        return instance
        
    def get(self, request, id):
        return Response()     