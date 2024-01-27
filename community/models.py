from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage as storage
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model

User = get_user_model()


class Board(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(default="")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="liked_boards"
    )

    def __str__(self):
        return self.title

class Comment(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="comments", null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100, null=True)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        self.title = self.board.title
        super(Comment, self).save(*args, **kwargs)
        
@receiver(post_save, sender=Board)
def update_comment_title(sender, instance, **kwargs):
    Comment.objects.filter(board=instance).update(title=instance.title)