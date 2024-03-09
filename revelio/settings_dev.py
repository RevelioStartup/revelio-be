"""
Django settings for revelio project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import environ
from datetime import timedelta

# Create environment variable
env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'authentication',
    'venue',
    'rest_framework',
    'rest_framework_simplejwt',
    'event',
    'ai',
    'vendor',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'revelio.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'revelio.wsgi.application'

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://revelio-two.vercel.app",
]

# Database
# Adapted from: https://medium.com/intelligentmachines/github-actions-end-to-end-ci-cd-pipeline-for-django-5d48d6f00abf


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'authentication.AppUser'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=480),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
    'SLIDING_TOKEN_LIFETIME': timedelta(days=30),
    'SLIDING_TOKEN_REFRESH_LIFETIME_LATE_USER': timedelta(days=1),
    'SLIDING_TOKEN_LIFETIME_LATE_USER': timedelta(days=30),
}

EMAIL_HOST = env('EMAIL_HOST')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')

PASSWORD_RESET_TIMEOUT = 300

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# STATIC_URL = 'static/'
DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
STATIC_URL = 'https://storage.googleapis.com/bucket-revelio-1/'
GS_BUCKET_NAME = 'bucket-revelio-1'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

import os
from pathlib import Path
from google.oauth2 import service_account

private_key = env("GCP_PRIVATE_KEY").replace("\\n", "\n")

gcs_credentials_info = {
    "type": "service_account",
    "project_id": env("GCP_PROJECT_ID"),
    "private_key_id": env("GCP_PRIVATE_KEY_ID"),
    "private_key": private_key,
    "client_email": env("GCP_CLIENT_EMAIL"),
    "client_id": env("GCP_CLIENT_ID"),
    "auth_uri": env("GCP_AUTH_URI"),
    "token_uri": env("GCP_TOKEN_URI"),
    "auth_provider_x509_cert_url": env("GCP_AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": env("GCP_CLIENT_X509_CERT_URL"),
    "universe_domain": env("GCP_UNIVERSE_DOMAIN")
}

GS_CREDENTIALS = service_account.Credentials.from_service_account_info(gcs_credentials_info)

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
        "OPTIONS": {
            "credentials": GS_CREDENTIALS,
            "bucket_name": os.getenv('GOOGLE_STORAGE_BUCKET'),
        },
    },
    "staticfiles": {
        "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
        "OPTIONS": {
            "credentials": GS_CREDENTIALS,
            "bucket_name": os.getenv('GOOGLE_STORAGE_BUCKET'),
        },
    }
}
