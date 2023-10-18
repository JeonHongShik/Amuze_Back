from django.contrib import admin
from .models import User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_per_page = 10


admin.site.register(User,UserAdmin)