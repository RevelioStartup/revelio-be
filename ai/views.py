from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.template.loader import render_to_string
from authentication.models import AppUser
from dotenv import load_dotenv
import re
import os
from openai import OpenAI

# load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'), organization=os.getenv('OPENAI_API_ORGANIZATION_ID'))

class AssistantView(APIView):

    permission_classes = ()

    def post(self, request):
        prompt = request.data.get('prompt')
        cleaned_prompt = re.sub(r'[^a-zA-Z0-9\s]', '', prompt)
        
        if len(cleaned_prompt.strip()) == 0:
            return Response(
                {
                    'msg': 'Make sure you are putting a correct prompt to the assistant.'
                }, status=400)

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt},
            ],
            temperature=1,
            max_tokens=256,
        )
        print(response)

        return Response({'msg' : response.choices[0].message.content})

class AutoFillView(APIView):
    
    permission_classes = ()

    def post(self, request):
        pass    