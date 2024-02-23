from authentication.models import AppUser
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
import re
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage

class RegisterView(APIView):
    
    permission_classes = ()

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        if AppUser.objects.filter(username = username).exists() or AppUser.objects.filter(email = email).exists():
            return Response({'msg': 'Username and/or email already taken!'}, status=400)
        validate_msg = self.validate_input(username, email, password)
        if validate_msg != 'valid':
            return Response({'msg': validate_msg}, status=400)
        new_user = AppUser.objects.create_user(email=email,username=username,password=password)
        new_user.save()
        user = authenticate(request, username=username,password=password)
        refresh = RefreshToken.for_user(user)
        return Response({'refresh': str(refresh),
                         'access': str(refresh.access_token)})

    def validate_input(self, username, email, password):
        if username == '' or password == '' or email == '':
            return 'Empty input! Make sure all the fields are filled.'
        if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email) is None:
            return 'Email format is wrong.'
        return 'valid'

class LoginView(APIView):

    permission_classes =()

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username,password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({'refresh': str(refresh),
                             'access': str(refresh.access_token)})
        else:
            return Response({'msg': 'Wrong username/password!'}, status=400)
        
class SendVerificationEmailView(APIView):

    permission_classes = ([IsAuthenticated])

    def get(self, request):
        return 'None'
    
    def post(self, request):
        return 'None'