from django.urls import path
from .views import Package

urlpatterns = [
    path('<int:id>/', Package.as_view(), name='package-detail'),
]
