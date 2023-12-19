from django.db import models
from django.conf import settings
import os
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete
from accounts.models import User



class WishType(models.Model):
    type = models.TextField(default="type")

    def __str__(self):
        return f"{self.type}"

class Image(models.Model):
    images = models.ImageField(upload_to="post/%y%m%d")

    def __str__(self):
        return f"{self.images}"



class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="post"
    )
    title = models.CharField(max_length=100)
    area = models.TextField()
    concert_type = models.TextField()
    wish_type = models.ManyToManyField(WishType, blank=True, related_name='posts')
    pay = models.BigIntegerField()
    deadline = models.CharField(max_length=50)
    playtime = models.CharField(max_length=50)
    content = models.TextField()
    image = models.ManyToManyField(Image, blank=True, related_name='posts', verbose_name='images')
    created_at = models.DateTimeField(auto_now_add=True)
    retouch_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author}님이 작성한 게시글 입니다."
    
    def get_favorited_users(self):
        return User.objects.filter(favorite__post=self)




@receiver(pre_save, sender=Post)
def delete_old_image(sender, instance, *args, **kwargs):
    if instance.pk:
        try:
            old_instance = Post.objects.get(pk=instance.pk)
        except Post.DoesNotExist:
            return
        else:
            old_images = old_instance.image.all()
            new_images = instance.image.all()
            for old_image in old_images:
                try:
                    old_path = old_image.images.path
                except ValueError:
                    return
                else:
                    if os.path.isfile(old_path):
                        if not new_images:
                            os.remove(old_path)
                        else:
                            for new_image in new_images:
                                try:
                                    new_path = new_image.images.path
                                except ValueError:
                                    os.remove(old_path)
                                else:
                                    if old_path != new_path:
                                        os.remove(old_path)



@receiver(post_delete, sender=Post)
def delete_profile_image(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False, many=True)