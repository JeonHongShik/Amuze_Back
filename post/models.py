from django.db import models
from django.conf import settings
import os
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete
from accounts.models import User

# Create your models here.


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="post"
    )
    title = models.CharField(max_length=100)
    area = models.TextField()
    concert_type = models.TextField()  # 공연 종류
    wish_type = models.TextField()  # 희망 무용 종류
    pay = models.BigIntegerField()  # 페이
    deadline = models.CharField(max_length=50)  # 공고 마감일
    playtime = models.CharField(max_length=50)  # 공연 날짜
    content = models.TextField()  # 공연 소개서
    image = models.ImageField(upload_to="post/%y%m%d")
    created_at = models.DateTimeField(auto_now_add=True)
    retouch_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author}님이 작성한 게시글 입니다."


@receiver(pre_save, sender=Post)
def delete_old_image(sender, instance, *args, **kwargs):
    if instance.pk:
        try:
            old_instance = Post.objects.get(pk=instance.pk)
        except Post.DoesNotExist:
            return
        else:
            try:
                old_path = old_instance.image.path
            except ValueError:
                return
            else:
                if os.path.isfile(old_path):
                    if not instance.image:
                        os.remove(old_path)
                    elif instance.image and hasattr(instance.image, "url"):
                        try:
                            new_path = instance.image.path
                        except ValueError:
                            os.remove(old_path)
                        else:
                            if old_path != new_path:
                                os.remove(old_path)


@receiver(post_delete, sender=Post)
def delete_profile_image(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)
