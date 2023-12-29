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

class Resume(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="resumes",null=True
    )
    title = models.CharField(max_length=20)
    gender = models.CharField(max_length=8)
    age = models.CharField(max_length=8)
    introduce = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    mainimage = models.FileField(upload_to="image/resume/%Y/%m/%d/", null=True, blank=True)
    otherimages1 = models.FileField(upload_to="image/resume/%Y/%m/%d/", null=True, blank=True)
    otherimages2 = models.FileField(upload_to="image/resume/%Y/%m/%d/", null=True, blank=True)
    otherimages3 = models.FileField(upload_to="image/resume/%Y/%m/%d/", null=True, blank=True)
    otherimages4 = models.FileField(upload_to="image/resume/%Y/%m/%d/", null=True, blank=True)

    # 이미지 이름 바꾸기 코드 짜기

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if self.pk:
            original_resume = Resume.objects.get(pk=self.pk)
            if original_resume.mainimage and original_resume.mainimage.name != self.mainimage.name:
                storage.delete(original_resume.mainimage.name)
            if original_resume.otherimages1 and original_resume.otherimages1.name != self.otherimages1.name:
                storage.delete(original_resume.otherimages1.name)
            if original_resume.otherimages2 and original_resume.otherimages2.name != self.otherimages2.name:
                storage.delete(original_resume.otherimages2.name)
            if original_resume.otherimages3 and original_resume.otherimages3.name != self.otherimages3.name:
                storage.delete(original_resume.otherimages3.name)
            if original_resume.otherimages4 and original_resume.otherimages4.name != self.otherimages4.name:
                storage.delete(original_resume.otherimages4.name)

        super().save(*args, **kwargs)

