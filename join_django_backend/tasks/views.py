from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from django.core import serializers
from .serializers import TaskSerializer
from tasks.models import Task

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
