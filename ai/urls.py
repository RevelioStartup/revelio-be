from django.urls import path
from ai.views import AssistantView, AutoFillView

app_name = 'ai'

urlpatterns = [
    path('autofill/', AutoFillView.as_view(), name='autofill'),
    path('assist/', AssistantView.as_view(), name='assist'),
]