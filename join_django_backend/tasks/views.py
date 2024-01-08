import json
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from django.core import serializers
from .serializers import TaskSerializer
from tasks.models import Task
from datetime import datetime

# Create your views here.
class TaskViewSet(viewsets.ModelViewSet):

    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]


    def get(self, request, format=None):
        #queryset = self.get_queryset(format=format)
        # Perform any additional filtering, pagination, etc., based on the request if needed
        #serialized_data = YourModelSerializer(queryset, many=True).data

        tasks = Task.objects.all()
        serialized_obj = serializers.serialize('json', [tasks, ]) 
        return HttpResponse(serialized_obj, content_type='application/json')
        #return Response(serialized_data)
    
    '''
    def get_queryset(self , format=None): 
        print("GET Request for Tasks")
        #tasks = Task.objects.all()
        #serialized_obj = serializers.serialize('json', tasks) 
        #return HttpResponse(serialized_obj, content_type='application/json')
        #return self.queryset
        return HttpResponse(self.queryset, content_type='application/json')
    '''
    
    def create(self, request):
        print(request.body)
        newTask = json.loads(request.body)
        print(newTask)
        
        date_str = newTask['dueDate']
        date_format = '%Y-%m-%d'

        date_obj = datetime.strptime(date_str, date_format)
        print(date_obj)


        task = Task.objects.create(title = newTask['title'], 
                                    description = newTask['description'], 
                                    category = newTask['category'],
                                    created_at = date_obj, 
                                    #assigned = newTask['assigned'],
                                    kanban = newTask['kanban'], 
                                    priority = newTask['priority'], 
                                    subtasks = newTask['subtasks'], 
                                    subtasksstatus = newTask['subtaskStatus'],
                                    ) 
        
        task.assigned.set()
        
        serialized_obj = serializers.serialize('json', [task, ]) 
    
        return HttpResponse(serialized_obj, content_type='application/json')
