from django.urls import path
from authentication.views import RegisterView, LoginView, SendVerificationEmailView, SendRecoverPasswordEmailView, ProfileView
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'authentication'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify/', SendVerificationEmailView.as_view(), name='verify_email'),
    path('recover/', SendRecoverPasswordEmailView.as_view(), name='recover_password'),
    path('profile/', ProfileView.as_view(), name='profile'),
]