import json
from django.http import JsonResponse
from authentication.models import *
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        email = data['email']
        new_user = AppUser.objects.create_user(email=email,username=username,password=password)
        new_user.save()
        return JsonResponse({'msg': 'Success! User registered'}, status=200)