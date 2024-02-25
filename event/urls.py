from django.urls import path

from event.views import EventList, EventDetail

app_name = 'event'

urlpatterns = [
    path('', EventDetail.as_view(), name='list'),
    path('<str:id>/', EventDetail.as_view(), name='detail'),
]
