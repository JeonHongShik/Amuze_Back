from django.utils.html import format_html
from django.contrib import admin
from .models import User


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['kakaoid','name','get_image']
    list_display_links = ['kakaoid']
    list_per_page = 10

    def get_image(self, obj):
        return format_html('<img src="{}" width="50" height="50" />', obj.profile.url)
    get_image.short_description = 'profile'
    
admin.site.register(User,UserAdmin)