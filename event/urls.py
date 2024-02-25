from django.urls import path

from event.views import EventView

app_name = 'event'

urlpatterns = [
    path('', EventView.as_view(), name='event_view'),
]
