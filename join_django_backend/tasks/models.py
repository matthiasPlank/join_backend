import datetime
from django.db import models

class Contact(models.Model): 
    firstName = models.CharField(max_length=64, blank=True)
    lastName = models.CharField(max_length=64, blank=True)
    email = models.CharField(max_length=64, blank=True)
    tel = models.CharField(max_length=64, blank=True)
    bgIconColor = models.CharField(max_length=64, blank=True)


# Create your models here.
class Task(models.Model): 
    title = models.CharField(max_length=256, blank=True)
    description = models.CharField(max_length=256, blank=True)
    created_at = models.DateField(default=datetime.date.today)
    category = models.CharField(max_length=64, blank=True)
    kanban = models.CharField(max_length=64, blank=True)
    priority = models.CharField(max_length=64, blank=True)
    assigned =  models.ManyToManyField(Contact, blank=True, related_name='assignees')
    subtasksstatus = models.JSONField(max_length=1024, blank=True)
    subtasks = models.JSONField(max_length=1024, blank=True)



