import ast
import json
from rest_framework import serializers

from .models import Task
class TaskSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
       # representation['assigned'] = representation['assigned'].replace("'", "\"")
        print( representation['assigned'])
        #representation['assigned'] = ast.literal_eval( representation['assigned'])

        return representation