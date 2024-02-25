from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.template.loader import render_to_string
from authentication.models import AppUser
import re

class AutoFillView(APIView):
    
    permission_classes = ([IsAuthenticated])

    def post(self, request):
        pass

class AssistantView(APIView):

    permission_classes = ([IsAuthenticated])

    def post(self, request):
        pass
        