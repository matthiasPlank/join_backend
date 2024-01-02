from django.shortcuts import render
from rest_framework import viewsets
from tasks.serializers import TaskSerializer

from tasks.models import Task

# Create your views here.
class TaskViewSet(viewsets.ModelViewSet):

    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]

    def get_queryset(self , format=None): 
        print("GET Request for Tasks")