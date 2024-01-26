from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from community.models import Board

# Create your models here.
class Notification(models.Model):
    uid = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    board_id = models.ForeignKey(Board, on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(auto_now_add=True)