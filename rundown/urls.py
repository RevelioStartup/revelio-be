from django.urls import path

from .views import (
    RundownCreateView,
)

urlpatterns = [
    path('', RundownCreateView.as_view(), name='rundown-create'),
]