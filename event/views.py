# Create your views here.
from rest_framework.views import APIView


class EventView(APIView):
    def get(self, request):
        raise NotImplementedError