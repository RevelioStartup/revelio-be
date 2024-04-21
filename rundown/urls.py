from django.urls import path

from .views import (
    RundownCreateView,
    RundownDetailView
)

urlpatterns = [
    path('', RundownCreateView.as_view(), name='rundown-create'),
    path('<uuid:id>', RundownDetailView.as_view(), name='rundown-detail'),
]