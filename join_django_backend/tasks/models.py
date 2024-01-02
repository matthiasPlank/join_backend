import datetime
from django.db import models

# Create your models here.
class Task(models.Model): 
    title = models.CharField(max_length=30)
    created_at = models.DateTimeField(default=datetime.date.today)