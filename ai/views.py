from dotenv import load_dotenv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveDestroyAPIView
from utils.permissions import IsOwner
from ai.models import RecommendationHistory
from ai.prompts import create_autofill_prompt, create_assistant_prompt
import re
import os
import json
from openai import OpenAI

from ai.serializers import RecommendationHistorySerializer

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'), organization=os.getenv('OPENAI_API_ORGANIZATION_ID'))

class AssistantView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        prompt = request.data.get('prompt')
        event = request.data.get('event')
        tipe = request.data.get('type')
        cleaned_prompt = re.sub(r'[^a-zA-Z0-9\s]', '', prompt)
        
        if len(cleaned_prompt.strip()) == 0:
            return Response(
                {
                    'msg': 'Make sure you are putting a correct prompt to the assistant.'
                }, status=400)

        if tipe == 'specific':
            full_prompt = create_assistant_prompt(prompt, event)
        else:
            full_prompt = prompt
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
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
                'prompt': prompt,
                'output': response['output'] if 'output' in response else '',
                'list': response['list'] if 'list' in response else [],
                'keyword': response['keyword'] if 'keyword' in response else [],
                'type': tipe
            }
        else :
            data = {
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

        return Response(data, status=200)

class HistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        history = RecommendationHistory.objects.select_related('user').filter(user = request.user)
        serializer = RecommendationHistorySerializer(history, many=True)
        for item in serializer.data:
            item['list'] = [i.strip().strip('"') for i in item['list'][1:-1].split(',') if i.strip().strip('"')]
            item['keyword'] = [i.strip().strip('"') for i in item['keyword'][1:-1].split(',') if i.strip().strip('"')]
        return Response(serializer.data)

class HistoryDetailView(RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request, id):
        history = RecommendationHistory.objects.get(pk=id)
        serializer = RecommendationHistorySerializer(history)
        data = serializer.data
        data['list'] = [i.strip().strip('"') for i in data['list'][1:-1].split(',') if i.strip().strip('"')]
        data['keyword'] = [i.strip().strip('"') for i in data['keyword'][1:-1].split(',') if i.strip().strip('"')]
        return Response(data)

class AutoFillView(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        form = request.data.get('event')
        if 'name' not in form or 'date' not in form or form['name'] == None or form['date'] == None:
            return Response({'msg' : 'Make sure you fill the required fields.'}, status=400)
        
        prompt = create_autofill_prompt(form)

        if not prompt:
            return Response({'msg': 'Make sure you are putting a correct form data.'}, status=400)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt},
            ],
            temperature=1,
            max_tokens=512,
        )

        return Response(json.loads(response.choices[0].message.content), status=200)  