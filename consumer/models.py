from django.db import models
from django.dispatch import receiver
from config import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver
import os

# Create your models here.


class consumer(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, null=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="consumer"
    )
    profile = models.ImageField(upload_to="consumer_profile/%y%m%d",null=True ,blank=True)
    age = models.CharField(max_length=10, null=True)
    education = models.CharField(max_length=100, null=True)
    career = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    retouch_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author}님이 작성한 글 입니다."
    
    
@receiver(pre_save, sender=consumer)
def delete_old_image(sender,instance,*args,**kwargs):
    if instance.pk:
        try:
            old_img = consumer.objects.get(pk=instance.pk).profile
        except consumer.DoesNotExist:
            return
        else:
            new_img = instance.profile
            if old_img and old_img.url != new_img.url:
                old_img_path = old_img.path
                os.remove(old_img_path)
        finally:
            pass