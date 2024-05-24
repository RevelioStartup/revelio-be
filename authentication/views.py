import sentry_sdk
from authentication.models import AppUser, Profile, UserToken
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .tokens import account_token
from .serializers import ProfileSerializer
from rest_framework import status
import asyncio
from django.core.exceptions import ObjectDoesNotExist
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils import timezone
from package.models import Package
from subscription.models import Subscription
from datetime import datetime
from rest_framework.parsers import MultiPartParser, FormParser
from authentication.utils import send_verification_email, send_recover_account_email, validate_input, create_shortened_token
from django.db.models import Q

class RegisterView(APIView):
    
    permission_classes = ()

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['username', 'password', 'email'],
        ),
        responses={
            200: 'Successful registration',
            400: 'Bad request'
        },
        operation_summary="Register a new user",
    )

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        
        validate_msg = validate_input(username, email, password)
        if validate_msg != 'valid':
            return Response({'msg': validate_msg}, status=400)
        AppUser.objects.filter(Q(email=email) | Q(username=username)).delete()
        new_user = AppUser.objects.create_user(username, email, password)
        Profile.objects.create(user=new_user)
        user = authenticate(request, username=new_user.username,password=password)
        refresh = RefreshToken.for_user(user)
        return Response({'refresh': str(refresh),
                         'access': str(refresh.access_token)})


class LoginView(APIView):

    permission_classes =()

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['username', 'password'],
        ),
        responses={
            200: 'Successful login',
            400: 'Wrong credentials'
        },
        operation_summary="Login existing user",
    )

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
            token = create_shortened_token(user)
            asyncio.run(send_verification_email(user, token.upper()))
            return Response({'msg': 'Email delivered!'})
    
    def post(self, request):
        user = request.user
        uid = user.pk
        short_token = request.data.get('token')
        user = AppUser.objects.get(pk=uid)
        if user is not None:
            try:
                short_token = short_token.lower()
                token = UserToken.objects.get(shortened_token=short_token, user=user).token
                UserToken.objects.filter(token=token).delete()
                if account_token.check_token(user, token):
                    user.is_verified_user = True
                    user.save()
                    Subscription.objects.create(user=user, plan=Package.objects.get(id=1), start_date=timezone.now(), end_date=timezone.make_aware(datetime(year=9999, month=12, day=31)))
                    return Response({'message': 'Email verified successfully!'}, status=200)
                else:
                    return Response({'msg': 'Expired token!'}, status=400)
            except ObjectDoesNotExist:
                return Response({'error': 'Invalid verification token!'}, status=400)
            except AttributeError:
                return Response({'error': 'Missing verification token!'}, status=400)

class SendRecoverPasswordEmailView(APIView):
    permission_classes =()

    swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['email'],
        ),
        responses={
            200: 'Password recovery email sent successfully',
            400: 'Bad request'
        },
        operation_summary="Send Password Recovery Email",
    )

    def post(self, request):
        email = request.data.get('email')
        is_user_exist = AppUser.objects.filter(email=email).exists()
        if is_user_exist:
            user = AppUser.objects.get(email=email)
            token = create_shortened_token(user).upper()
            asyncio.run(send_recover_account_email(user, token))
            return Response({'msg': 'Email delivered!'})
        else:
            return Response({"msg": "User with that email doesn't exist!"}, status=400)
    
    def put(self, request):
        email = request.data.get('email')
        short_token = request.data.get('token')
        new_password = request.data.get('new_password')
        is_user_exist = AppUser.objects.filter(email=email).exists()
        if is_user_exist:
            user = AppUser.objects.get(email=email)
            try:
                short_token = short_token.lower()
                token = UserToken.objects.get(shortened_token=short_token, user=user).token
                UserToken.objects.filter(token=token).delete()
                if account_token.check_token(user, token):
                    user.set_password(new_password)
                    user.save()
                    return Response({'msg': 'Password changes successfully!'}, status=200)
                else:
                    return Response({'msg': 'Expired token!'}, status=400)
            except ObjectDoesNotExist as e:
                sentry_sdk.capture_exception(e)
                return Response({'msg': 'Invalid verification token!'}, status=400)
            except AttributeError:
                return Response({'msg': 'Missing verification token!'}, status=400)
        else:
            return Response({'msg': "User doesn't exist!"}, status=400)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        responses={
            200: 'Profile retrieved successfully',
            400: 'Bad request'
        },
        operation_summary="Get Profile",
    )

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