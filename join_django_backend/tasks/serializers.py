import ast
import json
from rest_framework import serializers

from .models import Task, Contact
class TaskSerializer(serializers.HyperlinkedModelSerializer):

    assigned = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Task
        fields = '__all__'
    
    """
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        return representation
    """

class ContactSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'firstName' , 'lastName', 'email', 'tel', 'bgIconColor']
    