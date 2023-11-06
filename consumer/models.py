from django.db import models
from django.dispatch import receiver
from config import settings
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
import os

# Create your models here.


class consumer(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, null=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="consumer"
    )
    profile = models.ImageField(
        upload_to="consumer_image/%y%m%d", null=True, blank=True
    )
    age = models.CharField(max_length=10, null=True)
    education = models.CharField(max_length=100, null=True)
    career = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    retouch_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author}님이 작성한 글 입니다."


@receiver(pre_save, sender=consumer)
def delete_old_image(sender, instance, *args, **kwargs):
    if instance.pk:
        try:
            old_instance = consumer.objects.get(pk=instance.pk)
        except consumer.DoesNotExist:
            return
        else:
            # old_instance의 이미지가 실제로 존재하는지 확인
            try:
                old_path = old_instance.profile.path
            except ValueError:
                # 이미지가 없으면 path 속성에 접근할 수 없습니다.
                return
            else:
                if os.path.isfile(old_path):
                    # 이미지가 삭제되는 경우
                    if not instance.profile:
                        os.remove(old_path)
                    # 이미지가 변경되는 경우
                    elif instance.profile and hasattr(instance.profile, "url"):
                        try:
                            new_path = instance.profile.path
                        except ValueError:
                            os.remove(old_path)
                        else:
                            if old_path != new_path:
                                os.remove(old_path)


@receiver(post_delete, sender=consumer)
def delete_profile_image(sender, instance, **kwargs):
    if delete_profile_image:
        instance.profile.delete(save=False)
