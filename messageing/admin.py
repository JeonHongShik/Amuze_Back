from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id','uid', 'title','messagebody','content','board_id', 'created_at']
    search_fields = ['title', 'content', 'author__username']