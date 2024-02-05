from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from authentication.models import *

# Create your views here.
def returnTodoJson(request):
    data = Todo.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
