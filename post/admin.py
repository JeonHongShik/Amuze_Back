from django.contrib import admin
from .models import Post
from .models import WishType,Image


# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "content","author"]


admin.site.register(Post, PostAdmin)
admin.site.register(WishType)
admin.site.register(Image)