from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete
import os
from django.conf import settings


class Education(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    education = models.TextField()

    def __str__(self):
        return f"{self.education}"
    

class Experience(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    experience = models.TextField()
    
    def __str__(self):
        return f"{self.experience}"
    

class Award(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    award = models.TextField()

    def __str__(self):
        return f"{self.award}"
    

class Completion(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    completion = models.TextField()

    def __str__(self):
        return f"{self.completion}"
    

class Place(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    place = models.TextField()

    def __str__(self):
        return f"{self.place}"


class Resume(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="resume")
    phone = models.CharField(max_length=20) # 전화번호
    gender = models.CharField(max_length=8) # 성별
    age = models.IntegerField() # 나이
    education = models.ManyToManyField(Education) # 학력 - 배열
    experience = models.ManyToManyField(Experience) # 경력 내역 - 배열
    award = models.ManyToManyField(Award) # 수상 내역 - 배열
    completion = models.ManyToManyField(Completion) # 수료 - 배열
    introduce = models.TextField() # 자기소개
    place = models.ManyToManyField(Place) # 장소 - 배열
    image = models.ImageField(upload_to="resumes/%y%m%d/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.author)


@receiver(pre_save, sender=Resume)
def delete_old_image(sender, instance, *args, **kwargs):
    if instance.pk:
        try:
            old_instance = Resume.objects.get(pk=instance.pk)
        except Resume.DoesNotExist:
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


@receiver(post_delete, sender=Resume)
def delete_profile_image(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)
