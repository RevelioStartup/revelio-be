from rest_framework import generics, status
from utils.permissions import IsOwner
from django.db import transaction, IntegrityError

from task.models import Task
from .models import TaskStep
from .serializers import TaskStepSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
class TaskStepCreateListView(APIView):

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['task_id', 'steps'],
            properties={
                'task_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Task ID'),
                'steps': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    description='List of steps',
                    items=openapi.Items(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the step'),
                            'description': openapi.Schema(type=openapi.TYPE_STRING, description='Description of the step'),
                        }
                    )
                ),
            },
        ),
        responses={201: TaskStepSerializer(many=True), 400: 'Bad Request', 500: 'Internal Server Error'}
    )
    def post(self, request, *args, **kwargs):
        task_id = request.data.get('task_id')
        steps_data = request.data.get('steps', [])

        # Validate task existence
        task = get_object_or_404(Task, id=task_id)

        # Check if any TaskStep already exists for the task
        if TaskStep.objects.filter(task=task).exists():
            return Response({"error": "Task steps for the specified task already exist."}, status=status.HTTP_400_BAD_REQUEST)

        validated_steps_data = []
        errors = []

        for i, step_data in enumerate(steps_data, start=1):
            step_data['task'] = task.id
            step_data['step_order'] = i
            step_data['user'] = request.user.id
            step_data['status'] = "NOT_STARTED"

            serializer = TaskStepSerializer(data=step_data, context={'request': request})
            if serializer.is_valid():
                validated_steps_data.append(serializer.validated_data)
            else:
                errors.append(serializer.errors)

        # If there are any errors in any step, return the errors
        if errors:
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

        # If all steps are valid, perform bulk creation
        try:
            with transaction.atomic():
                created_steps = [TaskStep(**data) for data in validated_steps_data]  # Use the TaskStep model directly
                created_steps = TaskStep.objects.bulk_create(created_steps)

                result_serializer = TaskStepSerializer(created_steps, many=True, context={'request': request})
                return Response(result_serializer.data, status=status.HTTP_201_CREATED)

        except IntegrityError as e:
            return Response({"error": "Integrity error while creating task steps."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

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

