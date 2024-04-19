from django.urls import path

from .views import (
    RundownCreateView,
    RundownUpdateView
)

urlpatterns = [
    path('', RundownCreateView.as_view(), name='rundown-create'),
    path('update/<uuid:id>', RundownUpdateView.as_view(), name='rundown-update'),
]