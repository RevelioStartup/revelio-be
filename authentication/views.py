from django.shortcuts import render
import json
from django.http import JsonResponse
from authentication.models import *
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import re
from django.core.serializers import serialize

@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(View):
    def post(self, request):
        return 'None'