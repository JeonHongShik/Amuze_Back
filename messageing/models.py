from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from community.models import Board

# Create your models here.
class Notification(models.Model):
    uid = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
    title = models.ForeignKey(Board, on_delete=models.CASCADE)
    content = models.TextField()
    messagebody = models.TextField(null=True)
    board_id = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)