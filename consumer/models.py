from django.db import models


class Resume(models.Model):
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    gender = models.CharField(max_length=8)
    age = models.IntegerField()
    education = models.CharField(max_length=100)
    experience = models.TextField()
    award = models.TextField()
    introduce = models.TextField()
    photo = models.ImageField(upload_to="resumes/photo/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
