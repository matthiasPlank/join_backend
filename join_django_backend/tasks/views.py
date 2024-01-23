import json
import statistics
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from django.core import serializers
from .serializers import TaskSerializer, ContactSerializer
from tasks.models import Task
from datetime import datetime
from .models import Contact

from django.contrib.auth.decorators import login_required
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


# Create your views here.

class TaskViewSet(viewsets.ModelViewSet):

    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer
    
    # --------- DEACTIVATE CSFR TOKEN FOR PROJECT REVIEW ---------
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]

    """
    GET ALL TASKS Function
    """
    def get(self, request, format=None):
        try: 
            tasks = Task.objects.all()
            serialized_obj = serializers.serialize('json', [tasks, ]) 
            return HttpResponse(serialized_obj, content_type='application/json')
        except:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST )
     
    """
    CREATE NEW TASK Function
    """
    def post(self, request):
        newTask = json.loads(request.body)
        try:
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
                                        subtaskStatus = newTask['subtaskStatus'],
                                        ) 
            
            for contacts in newTask['assigned']: 
                task.assigned.add(Contact.objects.get(pk=contacts['id'])) 

            serialized_obj = serializers.serialize('json', [task, ]) 
            return HttpResponse(serialized_obj, content_type='application/json', status=status.HTTP_201_CREATED )
        
        except: 
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST )

    """
    UPDATES NEW TASK Function
    """
    def put(self, request, pk):
       
        editedTask = json.loads(request.body)
        try:
            instance = Task.objects.get(pk=pk)
        
            instance.assigned.clear(); 
            for contacts in editedTask['assigned']: 
                instance.assigned.add(Contact.objects.get(pk=contacts['id'])) 

            instance.save(); 
            serialized_obj = serializers.serialize('json', [instance, ]) 
            return HttpResponse(serialized_obj, content_type='application/json')
        
        except: 
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST )
        
    """
    UPDATES NEW TASK Function
    """
    def delete(self, request, pk, format=None):
        try: 
            task_to_delete = self.get_object(pk)
            task_to_delete.delete()
            return HttpResponse(status=status.HTTP_200_OK)
        except: 
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST )
        
        
class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    # --------- DEACTIVATE CSFR TOKEN FOR PROJECT REVIEW ---------
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]


    """
    CREATE NEW Contact Function
    """
    def create(self, request):
        newContact = json.loads(request.body)
        try:
            contact = Contact.objects.create(
                        firstName = newContact['firstName'], 
                        lastName = newContact['lastName'], 
                        email = newContact['email'], 
                        tel = newContact['tel'], 
                        bgIconColor = newContact['bgIconColor'], 
            )
            return HttpResponse(request.body, content_type='application/json', status=status.HTTP_201_CREATED)
        except: 
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST )
    
    """
    UPDATES Contact Function
    """
    def put(self, request, pk):
        editedContact = json.loads(request.body)
        try: 
            instance = Contact.objects.get(pk=pk)
            instance = editedContact
            instance.save(); 
            serialized_obj = serializers.serialize('json', [instance, ]) 
            return HttpResponse(serialized_obj, content_type='application/json')
        except: 
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST )

    """
    DELETE Contact Function
    """
    def delete(self, request, pk, format=None):
        try:
            contact_to_delete = self.get_object(pk)
            contact_to_delete.delete()
        except: 
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST )
        