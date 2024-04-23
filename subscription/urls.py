urlpatterns = [
    path('', TimelineCreateView.as_view(), name='timeline-create'),
    path('<uuid:pk>/', TimelineDetailView.as_view(), name='timeline-detail'),
]