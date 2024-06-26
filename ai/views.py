from dotenv import load_dotenv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveDestroyAPIView
from utils.permissions import IsOwner
from ai.models import RecommendationHistory
from ai.prompts import *
from ai.serializers import RecommendationHistorySerializer
from event.models import Event
from task.models import Task
import re
import os
import json
from openai import OpenAI
from utils.permissions import HasAIAssistant

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
AI_MODEL = 'gpt-3.5-turbo'

class AssistantView(APIView):

    permission_classes = [IsAuthenticated, HasAIAssistant]

    def post(self, request):
        prompt = request.data.get('prompt')
        event_id = request.data.get('event_id')
        tipe = request.data.get('type')

        if event_id == None or not Event.objects.get(pk=event_id):
            return Response(
                {
                    'msg': 'Event does not exist.'
                }, status=400)

        event_object = Event.objects.get(pk=event_id)
        cleaned_prompt = re.sub(r'[^a-zA-Z0-9\s]', '', prompt)
        if len(cleaned_prompt.strip()) == 0:
            return Response(
                {
                    'msg': 'Make sure you are putting a correct prompt to the assistant.'
                }, status=400)

        if tipe == 'specific':
            full_prompt = create_assistant_prompt(prompt, event_object)
        else:
            full_prompt = prompt
        
        response = client.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {"role": "user", "content": full_prompt},
            ],
            temperature=0.8,
            max_tokens=256,
        ).choices[0].message.content
        
        data = {}
        if tipe == 'specific':
            response = json.loads(response)
            data = {
                'event': event_id,
                'prompt': prompt,
                'output': response['output'] if 'output' in response else '',
                'list': response['list'] if 'list' in response else [],
                'keyword': response['keyword'] if 'keyword' in response else [],
                'type': tipe
            }
        else :
            data = {
                'event': event_id,
                'prompt': prompt,
                'output': response,
                'list': [],
                'keyword': [],
                'type': tipe
            }

        str_data = data.copy()
        str_data['list'] = json.dumps(str_data['list'])
        str_data['keyword'] = json.dumps(str_data['keyword'])
        serializer = RecommendationHistorySerializer(data=str_data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            data['id'] = serializer.data['id']
            data['date'] = serializer.data['date']

        return Response(data, status=200)

class HistoryView(APIView):
    permission_classes = [IsAuthenticated, HasAIAssistant]

    def get(self, request, event_id):
        history = RecommendationHistory.objects.filter(event=event_id)
        serializer = RecommendationHistorySerializer(history, many=True)
        for item in serializer.data:
            item['list'] = [i.strip().strip('"') for i in item['list'][1:-1].split(',') if i.strip().strip('"')]
            item['keyword'] = [i.strip().strip('"') for i in item['keyword'][1:-1].split(',') if i.strip().strip('"')]
        return Response(serializer.data)

class HistoryDetailView(RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwner, HasAIAssistant]

    def get(self, request, id):
        history = RecommendationHistory.objects.get(pk=id)
        serializer = RecommendationHistorySerializer(history)
        data = serializer.data
        data['list'] = [i.strip().strip('"') for i in data['list'][1:-1].split(',') if i.strip().strip('"')]
        data['keyword'] = [i.strip().strip('"') for i in data['keyword'][1:-1].split(',') if i.strip().strip('"')]
        return Response(data)

class AutoFillView(APIView):
    
    permission_classes = [IsAuthenticated, HasAIAssistant]

    def post(self, request):
        form = request.data.get('event')
        if 'name' not in form or 'date' not in form or form['name'] == None or form['date'] == None:
            return Response({'msg' : 'Make sure you fill the required fields.'}, status=400)
        
        prompt = create_autofill_prompt(form)

        if not prompt:
            return Response({'msg': 'Make sure you are putting a correct form data.'}, status=400)

        response = client.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {"role": "user", "content": prompt},
            ],
            temperature=1,
            max_tokens=512,
        )

        return Response(json.loads(response.choices[0].message.content), status=200)  
    
class TaskStepView(APIView):
    permission_classes = [IsAuthenticated, HasAIAssistant]

    def get(self, request, task_id):
        task_id = int(task_id)
        task = Task.objects.filter(id=task_id).first()
        if not task:
            return Response(
                {
                    'msg': 'Task not found.'
                }, status=400)
        
        event = Event.objects.get(id=task.event_id)

        prompt = create_task_steps_prompt(task, event)

        response = client.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {"role": "user", "content": prompt},
            ],
            temperature=0.8,
            max_tokens=256,
        ).choices[0].message.content

        response = json.loads(response)

        data = {
            'task_id': task_id,
            'steps': response['steps']
        }

        return Response(data, status=200)
    
class RundownView(APIView):
    permission_classes = [IsAuthenticated, HasAIAssistant]

    def get(self, request, event_id):
        event = Event.objects.filter(id=event_id).first()
        if not event:
            return Response(
                {
                    'msg': 'Event not found.'
                }, status=400)
        

        prompt = create_rundown_prompt(event)

        response = client.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {"role": "user", "content": prompt},
            ],
            temperature=0.8,
            max_tokens=256,
        ).choices[0].message.content

        response = json.loads(response)

        data = {
            'event_id': event_id,
            'rundown_data': response['rundown_data']
        }

        return Response(data, status=200)