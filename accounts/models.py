<<<<<<< HEAD
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

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
    profile = models.ImageField(upload_to="Userprofile/", null=True ,blank=True) 
    type = models.CharField(max_length=10,default='POST')  
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "kakaoid"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return f"{self.name}님의 계정 = {self.kakaoid}"

    def has_module_perms(self, app_label):  # 특정 어플리케이션에 대한 권한 확인
=======
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

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
    profile = models.ImageField(upload_to="Userprofile/", null=True ,blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "kakaoid"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return f"{self.name}님의 계정은 {self.kakaoid}"

    def has_module_perms(self, app_label):  # 특정 어플리케이션에 대한 권한 확인
>>>>>>> 449f363306bc1ffaec77f6392861278cbb95f3fa
        return True