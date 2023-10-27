from django.utils.html import format_html
from django.contrib import admin
from .models import consumer


# Register your models here.
class ConsumAdmin(admin.ModelAdmin):
    list_display = ['id','author','get_image','age','created_at','retouch_at']
    list_display_links = ['author']
    list_per_page = 10
    
    def get_image(self, obj):
        if obj.profile and obj.profile.url:
            return format_html('<img src="{}" width="50" />', obj.profile.url)
        else:
            return '이미지 없음'
    get_image.short_description = 'profile'
    
admin.site.register(consumer,ConsumAdmin)