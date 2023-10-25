<<<<<<< HEAD
from django.contrib import admin
from .models import User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_per_page = 10


=======
from django.contrib import admin
from .models import User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_per_page = 10


>>>>>>> 449f363306bc1ffaec77f6392861278cbb95f3fa
admin.site.register(User,UserAdmin)