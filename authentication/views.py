import json
from django.http import JsonResponse
from authentication.models import *
from django.contrib.auth import authenticate, login
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import re

@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        email = data['email']
        if AppUser.objects.filter(username = username).exists() or AppUser.objects.filter(email = email).exists():
            return JsonResponse({'msg': 'Username and/or email already taken!'}, status=400)
        validate_msg = Validators.validateInput(username, email, password)
        if validate_msg != 'valid':
            return JsonResponse({'msg': validate_msg}, status=400)
        new_user = AppUser.objects.create_user(email=email,username=username,password=password)
        new_user.save()
        return JsonResponse({'msg': 'Success! User registered'}, status=200)

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        user = authenticate(request, username=username,password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'msg': 'Success! User logged in'}, status=200)
        else:
            return JsonResponse({'msg': 'Wrong username/password!'}, status=400)

class Validators():
    def validateInput(username, email, password):
        if username == '' or password == '' or email == '':
            return 'Empty input! Make sure all the fields are filled.'
        if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email) is None:
            return 'Email format is wrong.'
        return 'valid'