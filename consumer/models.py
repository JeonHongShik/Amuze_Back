from django.db import models
from config import settings
from datetime import datetime

# Create your models here.


class consumer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="consumer"
    )
    call = models.CharField(max_length=50, null=True)
    age = models.CharField(max_length=10, null=True)
    education = models.CharField(max_length=100, null=True)
    career = models.CharField(max_length=100, null=True)
    
