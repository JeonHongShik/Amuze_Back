from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete
import os
from django.conf import settings
from django.core.files.storage import default_storage as storage


class Education(models.Model):
    resume = models.ForeignKey(
        "Resume", on_delete=models.CASCADE, related_name="educations"
    )
    education = models.TextField()

    def __str__(self):
        return f"{self.education}"


class Career(models.Model):
    resume = models.ForeignKey(
        "Resume", on_delete=models.CASCADE, related_name="careers"
    )
    career = models.TextField()

    def __str__(self):
        return f"{self.career}"


class Award(models.Model):
    resume = models.ForeignKey(
        "Resume", on_delete=models.CASCADE, related_name="awards"
    )
    award = models.TextField()

    def __str__(self):
        return f"{self.award}"


class Region(models.Model):
    resume = models.ForeignKey(
        "Resume", on_delete=models.CASCADE, related_name="regions"
    )
    region = models.TextField()

    def __str__(self):
        return f"{self.region}"


"""
class Image(models.Model):
    resume = models.ForeignKey(
        "Resume", on_delete=models.CASCADE, related_name="photo"
    )
    photo = models.FileField(upload_to="image/%Y/%m/%d/")

    def __str__(self):
        return str(self.photo)
"""


class Resume(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="resumes"
    )
    title = models.CharField(max_length=20)
    gender = models.CharField(max_length=8)
    age = models.CharField(max_length=8)
    introduce = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile_image = models.FileField(upload_to="image/%Y/%m/%d/", null=True, blank=True)
    image1 = models.FileField(upload_to="image/%Y/%m/%d/", null=True, blank=True)
    image2 = models.FileField(upload_to="image/%Y/%m/%d/", null=True, blank=True)
    image3 = models.FileField(upload_to="image/%Y/%m/%d/", null=True, blank=True)
    image4 = models.FileField(upload_to="image/%Y/%m/%d/", null=True, blank=True)

    # 이미지 이름 바꾸기 코드 짜기

    def __str__(self):
        return str(self.author)

    def save(self, *args, **kwargs):
        if self.pk:
            original_resume = Resume.objects.get(pk=self.pk)
            if original_resume.profile_image.name != self.profile_image.name:
                storage.delete(original_resume.profile_image.name)
            if original_resume.image1.name != self.image1.name:
                storage.delete(original_resume.image1.name)
            if original_resume.image2.name != self.image2.name:
                storage.delete(original_resume.image2.name)
            if original_resume.image3.name != self.image3.name:
                storage.delete(original_resume.image3.name)
            if original_resume.image4.name != self.image4.name:
                storage.delete(original_resume.image4.name)

        super().save(*args, **kwargs)


"""
@receiver(pre_save, sender=Image)
def delete_old_image(sender, instance, *args, **kwargs):
    if instance.pk:
        try:
            old_instance = Image.objects.get(pk=instance.pk)
        except Image.DoesNotExist:
            return
        else:
            try:
                old_path = old_instance.photo.path
            except ValueError:
                return
            else:
                if os.path.isfile(old_path):
                    if not instance.photo:
                        os.remove(old_path)
                    elif instance.photo and hasattr(instance.photo, "url"):
                        try:
                            new_path = instance.photo.path
                        except ValueError:
                            os.remove(old_path)
                        else:
                            if old_path != new_path:
                                os.remove(old_path)


@receiver(post_delete, sender=Image)
def delete_profile_image(sender, instance, **kwargs):
    if instance.photo:
        instance.photo.delete(save=False)
"""
