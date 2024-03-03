from dotenv import load_dotenv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveDestroyAPIView
from django.urls import reverse
from django.shortcuts import redirect
from utils.permissions import IsOwner
from ai.prompts import create_autofill_prompt
from ai.models import RecommendationHistory
from ai.serializers import RecommendationHistorySerializer
import re
import os
import json
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'), organization=os.getenv('OPENAI_API_ORGANIZATION_ID'))

class AssistantView(APIView):

    def post(self, request):
        prompt = request.data.get('prompt')
        cleaned_prompt = re.sub(r'[^a-zA-Z0-9\s]', '', prompt)
        
        if len(cleaned_prompt.strip()) == 0:
            return Response(
                {
                    'msg': 'Make sure you are putting a correct prompt to the assistant.'
                }, status=400)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt},
            ],
            temperature=1,
            max_tokens=256,
        )

        data = {
            'prompt' : prompt,
            'output' : response.choices[0].message.content
        }

        serializer = RecommendationHistorySerializer(data=data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()

        return Response({'msg' : response.choices[0].message.content})

class HistoryView(APIView):

    def get(self, request):
        history = RecommendationHistory.objects.select_related('user').filter(user = request.user)
        serializer = RecommendationHistorySerializer(history, many=True)
        
        return Response(serializer.data)

class HistoryDetailView(RetrieveDestroyAPIView):
    queryset = RecommendationHistory.objects.all()
    serializer_class = RecommendationHistorySerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated, IsOwner]

class AutoFillView(APIView):
    
    permission_classes = ()

    def post(self, request):
        form = request.data.get('form')
        if 'name' in form and 'date' in form and 'budget' in form:
            name, date, budget = form['name'], form['date'], form['budget']
        else:
            return Response({'msg': 'Make sure you are putting a correct form data.'}, status=400)

        prompt = create_autofill_prompt(name, date, budget)
        if not prompt:
            return Response({'msg' : 'Make sure you fill the required fields.'}, status=400)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt},
            ],
            temperature=1,
            max_tokens=512,
        )

        return Response(json.loads(response.choices[0].message.content), status=200)