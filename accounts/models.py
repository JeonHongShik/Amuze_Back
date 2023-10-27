from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
import os

class UserManager(BaseUserManager):
    def create_user(self, kakaoid, name, password=None):
        user = self.model(kakaoid=kakaoid, name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,kakaoid,name,password):
        user = self.create_user(kakaoid=kakaoid,name=name,password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser , PermissionsMixin):
    kakaoid = models.CharField(unique=True,max_length=100)
    name = models.CharField(max_length=50,default="name")
    profile = models.ImageField(upload_to="Userprofile/%Y%m%d", null=True ,blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    retouch_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "kakaoid"
    REQUIRED_FIELDS = ["name"]

    def has_module_perms(self, app_label):  # 특정 어플리케이션에 대한 권한 확인
        return True
    
@receiver(pre_save, sender=User)
def delete_old_image(sender,instance,*args,**kwargs):
    if instance.pk:
        try:
            old_img = User.objects.get(pk=instance.pk).profile
        except User.DoesNotExist:
            return
        else:
            new_img = instance.profile
            if old_img and old_img.url != new_img.url:
                old_img_path = old_img.path
                os.remove(old_img_path)
        finally:
            pass