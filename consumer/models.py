from django.db import models
from config import settings
from datetime import datetime

# Create your models here.


class consumer(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, null=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="consumer"
    )
    age = models.CharField(max_length=10, null=True)
    education = models.CharField(max_length=100, null=True)
    career = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    retouch_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author}님이 작성한 글 입니다."