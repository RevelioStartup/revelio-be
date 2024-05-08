from django.urls import path

from .views import (
    RundownCreateView,
    RundownDetailView,
    RundownListView,
    DeleteAllRundownView
)

urlpatterns = [
    path('', RundownCreateView.as_view(), name='rundown-create'),
    path('<uuid:id>', RundownDetailView.as_view(), name='rundown-detail'),
    path('events/<uuid:event_id>/', RundownListView.as_view(), name='rundown-list'),
    path('events/<uuid:event_id>/delete/', DeleteAllRundownView.as_view(), name='rundown-delete-all'),
]