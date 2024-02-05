from django.urls import path
from authentication.views import *

app_name = 'authentication'

urlpatterns = [
    path('try', returnTodoJson, name='returnTodoJson'),
]