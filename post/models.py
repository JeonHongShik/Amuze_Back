from django.db import models
from django.conf import settings
import os
from django.dispatch import receiver
from django.db.models.signals import pre_save
from accounts.models import User

class Image(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='images')
    photos = models.FileField(upload_to="post/%y%m%d", blank=True)

    def __str__(self):
        return f"{self.photos}" if self.photos else "No photo"

class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="post"
    )
    title = models.CharField(max_length=100)
    region  = models.TextField()
    type = models.TextField(default="type")
    pay = models.TextField()
    wishtype = models.TextField(default="type")
    deadline = models.CharField(max_length=50)
    datetime = models.CharField(max_length=50)
    introduce = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    retouch_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author}님이 작성한 {self.title} 입니다."
    
    def get_favorited_users(self):
        return User.objects.filter(favorite__post=self)


@receiver(pre_save, sender=Image)
def delete_old_image(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_image = Image.objects.get(pk=instance.pk)
            if old_image.photos and old_image.photos != instance.photos:
                old_image.photos.delete(save=False)
        except Image.DoesNotExist:
            return