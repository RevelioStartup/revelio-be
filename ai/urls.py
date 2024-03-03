from django.urls import path
from ai.views import AssistantView, AutoFillView, HistoryView, HistoryDetailView

app_name = 'ai'

urlpatterns = [
    path('autofill/', AutoFillView.as_view(), name='autofill'),
    path('assistant/', AssistantView.as_view(), name='assistant'),
    path('history/', HistoryView.as_view(), name='history'),
    path('history/<uuid:id>/', HistoryDetailView.as_view(), name='history-detail'),
]