from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete
import os
from django.conf import settings


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


class Image(models.Model):
    resume = models.ForeignKey(
        "Resume", on_delete=models.CASCADE, related_name="photos"
    )
    photo = models.FileField(upload_to="image/%Y/%m/%d/")

    def __str__(self):
        return str(self.photo)


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

    def __str__(self):
        return str(self.author)

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
