from django.urls import path
from ai.views import AssistantView, AutoFillView, HistoryView, HistoryDetailView, TaskStepView

app_name = 'ai'

urlpatterns = [
    path('autofill/', AutoFillView.as_view(), name='autofill'),
    path('assistant/', AssistantView.as_view(), name='assistant'),
    path('history/all/<str:event_id>/', HistoryView.as_view(), name='history'),
    path('history/<str:id>/', HistoryDetailView.as_view(), name='history-detail'),
    path('task-steps/', TaskStepView.as_view(), name='ai-task-steps'),
]