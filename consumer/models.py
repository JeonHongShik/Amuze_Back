from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete
import os
from django.conf import settings


class Education(models.Model):
    resume = models.ForeignKey(
        "Resume", on_delete=models.CASCADE, related_name="educations_resumes"
    )
    education = models.TextField()

    def __str__(self):
        return f"{self.education}"


class Career(models.Model):
    resume = models.ForeignKey(
        "Resume", on_delete=models.CASCADE, related_name="careers_resumes"
    )
    career = models.TextField()

    def __str__(self):
        return f"{self.career}"


class Award(models.Model):
    resume = models.ForeignKey(
        "Resume", on_delete=models.CASCADE, related_name="awards_resumes"
    )
    award = models.TextField()

    def __str__(self):
        return f"{self.award}"


class Region(models.Model):
    resume = models.ForeignKey(
        "Resume", on_delete=models.CASCADE, related_name="regions_resumes"
    )
    region = models.TextField()

    def __str__(self):
        return f"{self.region}"


class Image(models.Model):
    photo = models.FileField(upload_to="image/%Y/%m/%d/")

    def __str__(self):
        return str(self.photo)


class Resume(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="resume"
    )
    title = models.CharField(max_length=20)  # 제목
    gender = models.CharField(max_length=8)  # 성별
    age = models.CharField(max_length=8)  # 나이
    regions = models.ManyToManyField(Region, related_name="resumes")  # 지역
    educations = models.ManyToManyField(Education, related_name="resumes")  # 학력 및 전공
    careers = models.ManyToManyField(Career, related_name="resumes")  # 경력
    awards = models.ManyToManyField(Award, related_name="resumes")  # 수상 이력
    introduce = models.TextField()  # 자기소개
    photos = models.FileField(upload_to="image/%Y/%m/%d/", blank=True)
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
                old_path = old_instance.photos.path
            except ValueError:
                return
            else:
                if os.path.isfile(old_path):
                    if not instance.photos:
                        os.remove(old_path)
                    elif instance.photos and hasattr(instance.photos, "url"):
                        try:
                            new_path = instance.photos.path
                        except ValueError:
                            os.remove(old_path)
                        else:
                            if old_path != new_path:
                                os.remove(old_path)


@receiver(post_delete, sender=Resume)
def delete_profile_image(sender, instance, **kwargs):
    if instance.photos:
        instance.photos.delete(save=False)
