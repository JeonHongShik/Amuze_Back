from django.contrib import admin
from .models import bookmark

class bookmarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']
    list_filter = ['user', 'post', 'created_at']
    search_fields = ['user__name', 'post__title']

admin.site.register(bookmark, bookmarkAdmin)
