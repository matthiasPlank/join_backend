import json
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from django.core import serializers
from .serializers import TaskSerializer, ContactSerializer
from tasks.models import Task
from datetime import datetime
from .models import Contact

# Create your views here.
class TaskViewSet(viewsets.ModelViewSet):

    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]


    def get(self, request, format=None):
        tasks = Task.objects.all()
        serialized_obj = serializers.serialize('json', [tasks, ]) 
        return HttpResponse(serialized_obj, content_type='application/json')
     

    def create(self, request):
        newTask = json.loads(request.body)
    
        date_str = newTask['dueDate']
        date_format = '%Y-%m-%d'
        date_obj = datetime.strptime(date_str, date_format)
    
        task = Task.objects.create( 
                                    title = newTask['title'], 
                                    description = newTask['description'], 
                                    category = newTask['category'],
                                    created_at = date_obj, 
                                    kanban = newTask['kanban'], 
                                    priority = newTask['priority'], 
                                    subtasks = newTask['subtasks'], 
                                    subtasksstatus = newTask['subtaskStatus'],
                                    ) 
        
        for contacts in newTask['assigned']: 
            task.assigned.add(Contact.objects.get(pk=contacts['id'])) 

        serialized_obj = serializers.serialize('json', [task, ]) 
    
        return HttpResponse(serialized_obj, content_type='application/json')

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer