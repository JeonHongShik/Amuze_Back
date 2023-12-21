from django.db import models
from django.conf import settings
import os
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete
from django.core.files import File
from accounts.models import User
from datetime import datetime

class WishType(models.Model):
    type = models.TextField(default="type")
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='wish_types')

    def __str__(self):
        return f"{self.type}"


def get_image_filename(instance, filename):
    today = datetime.now()
    date = today.strftime("%Y_%m_%d")

    last_image = Image.objects.last()
    if last_image is not None:
        img_id = last_image.id + 1
    else:
        img_id = 1

    extension = filename.split('.')[-1]

    new_filename = f"{date}_{instance.post.author}_{instance.post.title}_{img_id}.{extension}"

    return os.path.join('post', new_filename)


class Image(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='images')
    images = models.ImageField(upload_to=get_image_filename)

    def __str__(self):
        return f"{self.images}"

class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="post"
    )
    title = models.CharField(max_length=100)
    area = models.TextField()
    concert_type = models.TextField()
    pay = models.BigIntegerField()
    deadline = models.CharField(max_length=50)
    playtime = models.CharField(max_length=50)
    content = models.TextField()
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
            if old_image.images and old_image.images != instance.images:
                old_image.images.delete(save=False)
        except Image.DoesNotExist:
            return