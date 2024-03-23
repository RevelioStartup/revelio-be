from rest_framework import generics, status
from .models import TaskStep
from .serializers import TaskStepSerializer
from rest_framework.response import Response


class TaskStepListCreateView(generics.ListCreateAPIView):
    queryset = TaskStep.objects.all()
    serializer_class = TaskStepSerializer

class TaskStepDestroyView(generics.DestroyAPIView): #Delete a single test step
    queryset = TaskStep.objects.all()
    serializer_class = TaskStepSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Task step successfully deleted."}, 
            status=status.HTTP_200_OK
        )

class DeleteAllTaskStepsView(generics.GenericAPIView):
    queryset = TaskStep.objects.all()

    def delete(self, request, *args, **kwargs):
        task_id = kwargs.get('task_id')
        deleted_count, _ = TaskStep.objects.filter(task_id=task_id).delete()  # This also returns the number of deleted objects
        return Response(
            {"message": f"Successfully deleted {deleted_count} task step(s)."}, 
            status=status.HTTP_200_OK
        )