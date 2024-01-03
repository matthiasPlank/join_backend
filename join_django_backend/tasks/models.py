import datetime
from django.db import models
from django.contrib.postgres.fields import ArrayField



# Create your models here.
class Task(models.Model): 
    title = models.CharField(max_length=64, blank=True)
    description = models.CharField(max_length=256, blank=True)
    created_at = models.DateField(default=datetime.date.today)
    category = models.CharField(max_length=64, blank=True)
    kanban = models.CharField(max_length=64, blank=True)
    priority = models.CharField(max_length=64, blank=True)
    assigned =  models.CharField(max_length=1024, blank=True)
    subtasksstatus = models.CharField(max_length=1024, blank=True)
    subtasks = models.CharField(max_length=1024, blank=True)