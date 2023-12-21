from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete
import os
from django.conf import settings


class Education(models.Model):
    resume = models.ForeignKey("Resume", on_delete=models.CASCADE)
    education = models.TextField()

    def __str__(self):
        return f"{self.education}"


class Career(models.Model):
    resume = models.ForeignKey("Resume", on_delete=models.CASCADE)
    career = models.TextField()

    def __str__(self):
        return f"{self.career}"


class Award(models.Model):
    resume = models.ForeignKey("Resume", on_delete=models.CASCADE)
    award = models.TextField()

    def __str__(self):
        return f"{self.award}"


class Completion(models.Model):
    resume = models.ForeignKey("Resume", on_delete=models.CASCADE)
    completion = models.TextField()

    def __str__(self):
        return f"{self.completion}"


class Region(models.Model):
    resume = models.ForeignKey("Resume", on_delete=models.CASCADE)
    region = models.TextField()

    def __str__(self):
        return f"{self.region}"


class Image(models.Model):
    image = models.ImageField(upload_to="image/%Y/%m/%d/")

    def __str__(self):
        return str(self.image)


class Resume(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="resume"
    )
    name = models.CharField(max_length=20)  # 이름
    gender = models.CharField(max_length=8)  # 성별
    age = models.CharField(max_length=8)  # 나이
    region = models.ManyToManyField(Region)  # 지역
    edu_background = models.ManyToManyField(Education)  # 학력 및 전공
    career = models.ManyToManyField(Career)  # 경력
    awarded = models.ManyToManyField(Award)  # 수상 이력
    introduce = models.TextField()  # 자기소개
    image = models.ManyToManyField(Image, blank=True)
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
