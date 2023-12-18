from django.contrib import admin
from .models import Post
from .models import WishType,Image


# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "content","author",'display_wish_type']

    def display_wish_type(self, obj):
        return ', '.join([wish_type.type for wish_type in obj.wish_type.all()])

    display_wish_type.short_description = 'Wish Types'

admin.site.register(Post, PostAdmin)
admin.site.register(WishType)
admin.site.register(Image)