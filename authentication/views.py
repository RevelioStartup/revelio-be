from authentication.models import AppUser, Profile
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
import re
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import account_token
from django.core.mail import EmailMessage
from .serializers import ProfileSerializer
from rest_framework import status
import asyncio

async def send_verification_email(user):
    username = user.username
    email = user.email
    subject = "Revelio - Verify Email"
    message = render_to_string('verify_email_msg.html', {
        'username': username,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':account_token.make_token(user),
    })
    email = EmailMessage(
        subject, message, to=[email]
    )
    email.content_subtype = 'html'
    email.send()

async def send_recover_account_email(user):
    email = user.email
    subject = "Revelio - Password Recovery Email"
    message = render_to_string('change_password_email_msg.html', {
        'token':account_token.make_token(user),
    })
    email = EmailMessage(
        subject, message, to=[email]
    )
    email.content_subtype = 'html'
    email.send()


def validate_input(username, email, password):
    if username.strip() == '' or password.strip() == '' or email.strip() == '':
        return 'Empty input! Make sure all the fields are filled.'
    if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email) is None:
        return 'Email format is wrong.'
    return 'valid'

from rest_framework.parsers import MultiPartParser, FormParser

class RegisterView(APIView):
    
    permission_classes = ()

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        if username is None or password is None or email is None:
            return Response({'msg': 'One or more fields are missing!'}, status= 400)
        if AppUser.objects.filter(username = username).exists() or AppUser.objects.filter(email = email).exists():
            return Response({'msg': 'Username and/or email already taken!'}, status=400)
        validate_msg = validate_input(username, email, password)
        if validate_msg != 'valid':
            return Response({'msg': validate_msg}, status=400)
        new_user = AppUser.objects.create_user(email=email,username=username,password=password)
        new_user.save()
        Profile.objects.create(user=new_user)
        user = authenticate(request, username=username,password=password)
        refresh = RefreshToken.for_user(user)
        return Response({'refresh': str(refresh),
                         'access': str(refresh.access_token)})


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
        if request.user.is_verified_user != True:
            user = request.user
            asyncio.run(send_verification_email(user))
            return Response({'msg': 'Email delivered!'})
    
    def post(self, request):
        user = request.user
        uid = user.pk
        token = request.data.get('token')
        user = AppUser.objects.get(pk=uid)
        if user is not None and account_token.check_token(user, token):
            user.is_verified_user = True
            user.save()
            return Response({'message': 'Email verified successfully!'}, status=200)
        else:
            return Response({'error': 'Invalid verification token!'}, status=400)

class SendRecoverPasswordEmailView(APIView):
    permission_classes =()

    def post(self, request):
        email = request.data.get('email')
        is_user_exist = AppUser.objects.filter(email=email).exists()
        if is_user_exist:
            user = AppUser.objects.get(email=email)
            asyncio.run(send_recover_account_email(user))
            return Response({'msg': 'Email delivered!'})
        else:
            return Response({"msg": "User with that email doesn't exist!"}, status=400)
    
    def put(self, request):
        email = request.data.get('email')
        token = request.data.get('token')
        new_password = request.data.get('new_password')
        is_user_exist = AppUser.objects.filter(email=email).exists()
        if is_user_exist:
            user = AppUser.objects.get(email=email)
            if user is not None and account_token.check_token(user, token):
                user.set_password(new_password)
                user.save()
                return Response({'msg': 'Password changes successfully!'}, status=200)
            else:
                return Response({'msg': 'Invalid verification token!'}, status=400)
        else:
            return Response({'msg': "User doesn't exist!"}, status=400)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile

    def get(self, request, *args, **kwargs):
        profile = self.get_object()
        user_data = {
            'id': request.user.id,
            'username': request.user.username,
            'email': request.user.email,
        }
        profile_data = self.serializer_class(profile).data
        return Response({'user': user_data, 'profile': profile_data})

    def put(self, request):
        profile = self.get_object()
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)