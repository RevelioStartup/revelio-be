from rest_framework import generics

from utils.permissions import IsEventOwner, IsOwner
from .models import Task
from .serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated
from utils.permissions import HasEventTracker

class TaskCreateView(generics.CreateAPIView):
    permission_classes=[IsAuthenticated, IsEventOwner, HasEventTracker]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class SeeTaskListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsEventOwner, HasEventTracker]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        event_id = self.kwargs['event_id']
        return Task.objects.filter(event_id=event_id)

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsEventOwner, HasEventTracker]
    lookup_url_kwarg = 'task_id'
    serializer_class = TaskSerializer
    
    def get_queryset(self):
        return Task.objects.filter(event_id=self.kwargs['event_id'], id=self.kwargs['task_id'])
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)