from rest_framework import generics, status

from utils.permissions import IsOwner
from .models import TaskStep
from .serializers import TaskStepSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class TaskStepCreateView(generics.CreateAPIView):
    queryset = TaskStep.objects.all()
    serializer_class = TaskStepSerializer

    def get(self, request, *args, **kwargs):
        # This method handles GET requests, returning a list of task steps
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
class TaskStepUpdateView(generics.UpdateAPIView):
    queryset = TaskStep.objects.all()
    serializer_class = TaskStepSerializer
    permission_classes = [IsOwner, IsAuthenticated]

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

class TaskStepDestroyView(generics.DestroyAPIView):
    queryset = TaskStep.objects.all()
    serializer_class = TaskStepSerializer
    permission_classes = [IsOwner, IsAuthenticated]  # Apply the custom permission class

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Task step successfully deleted."}, 
            status=status.HTTP_200_OK
        )

class DeleteAllTaskStepsView(generics.GenericAPIView):
    queryset = TaskStep.objects.all()
    permission_classes = [IsOwner, IsAuthenticated]  

    def delete(self, request, *args, **kwargs):
        task_id = kwargs.get('task_id')
        task_steps = TaskStep.objects.filter(task_id=task_id)
        deleted_count, _ = task_steps.delete()
        return Response(
            {"message": f"Successfully deleted {deleted_count} task step(s)."}, 
            status=status.HTTP_200_OK
        )

