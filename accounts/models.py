from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
import os

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,name,password):
        user = self.create_user(email=email,name=name,password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser , PermissionsMixin):
    email = models.EmailField(primary_key=True , unique=True , default="default@email.com")
    kakao_id = models.TextField(unique=True, null=True , blank=True)
    apple_id = models.TextField(unique=True, null=True , blank=True)
    name = models.CharField(max_length=50, default="name")
    profile = models.ImageField(upload_to="Userprofile/%Y%m%d",null=True ,blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    retouch_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self) -> str:
        return self.name
    
    def has_module_perms(self, app_label):  # 특정 어플리케이션에 대한 권한 확인
        return True
    
@receiver(pre_save, sender=User)
def delete_old_image(sender, instance, *args, **kwargs):
    if instance.pk:
        try:
            old_instance = User.objects.get(pk=instance.pk)
        except User.DoesNotExist:
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
                    elif instance.profile and hasattr(instance.profile, 'url'):
                        try:
                            new_path = instance.profile.path
                        except ValueError:
                            os.remove(old_path)
                        else:
                            if old_path != new_path:
                                os.remove(old_path)

@receiver(post_delete, sender=User)
def delete_profile_image(sender, instance , **kwargs):
    if delete_profile_image:
        instance.profile.delete(save=False)