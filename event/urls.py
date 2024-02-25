from django.urls import path

from event.views import EventList, EventDetail

app_name = 'event'

urlpatterns = [
    path('', EventList.as_view(), name='list'),
    path('<uuid:id>/', EventDetail.as_view(), name='detail'),
]
