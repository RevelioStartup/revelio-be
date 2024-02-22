import json
from django.http import JsonResponse
from authentication.models import *
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
        if username == '' or password == '' or email == '':
            return JsonResponse({'msg': 'Empty input! Make sure all the fields are filled.'}, status=400)
        if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email) is None:
            return JsonResponse({'msg': 'Email format is wrong.'}, status=400)
        new_user = AppUser.objects.create_user(email=email,username=username,password=password)
        new_user.save()
        return JsonResponse({'msg': 'Success! User registered'}, status=200)