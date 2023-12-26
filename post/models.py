from django.db import models
from django.conf import settings
import os
from django.dispatch import receiver
from django.db.models.signals import pre_save
from accounts.models import User
from django.core.files.storage import default_storage as storage

class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="post",null=True
    )
    title = models.CharField(max_length=100,null=True)
    region  = models.TextField(null=True)
    type = models.TextField(default="type",null=True)
    pay = models.TextField(null=True)
    wishtype = models.TextField(default="type",null=True)
    deadline = models.CharField(max_length=50,null=True)
    datetime = models.CharField(max_length=50,null=True)
    introduce = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    retouch_at = models.DateTimeField(auto_now=True)
    mainimage = models.FileField(upload_to="image/%Y/%m/%d/",null=True,blank=True)
    otherimages1 = models.FileField(upload_to="image/%Y/%m/%d/",null=True,blank=True)
    otherimages2 = models.FileField(upload_to="image/%Y/%m/%d/",null=True,blank=True)
    otherimages3 = models.FileField(upload_to="image/%Y/%m/%d/",null=True,blank=True)
    otherimages4 = models.FileField(upload_to="image/%Y/%m/%d/",null=True,blank=True)


        #이미지 이름 바꾸기 코드 짜기
    
    def __str__(self):
        return f"{self.author}님이 작성한 {self.title} 입니다."
    
    def get_favorited_users(self):
        return User.objects.filter(favorite__post=self)
    
    def save(self, *args, **kwargs):
        if self.pk:
            original_post = Post.objects.get(pk=self.pk)
            if original_post.mainimage.name != self.mainimage.name:
                storage.delete(original_post.mainimage.name)
            if original_post.otherimages1.name != self.otherimages1.name:
                storage.delete(original_post.otherimages1.name)
            if original_post.otherimages2.name != self.otherimages2.name:
                storage.delete(original_post.otherimages2.name)
            if original_post.otherimages3.name != self.otherimages3.name:
                storage.delete(original_post.otherimages3.name)
            if original_post.otherimages4.name != self.otherimages4.name:
                storage.delete(original_post.otherimages4.name)

        super().save(*args, **kwargs)