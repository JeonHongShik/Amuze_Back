from django.contrib import admin
from .models import Post
from .models import wishtype,Image


# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "introduce","author"]


admin.site.register(Post, PostAdmin)
admin.site.register(wishtype)
admin.site.register(Image)