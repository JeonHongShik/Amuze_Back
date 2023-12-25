from django.contrib import admin
from .models import Postbookmark,Resumebookmark,Boardbookmark

class PostbookmarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']
    list_filter = ['user', 'post', 'created_at']


class ResumebookmarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'resume', 'created_at']
    list_filter = ['user', 'resume', 'created_at']

class BoardbookmarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'board', 'created_at']
    list_filter = ['user', 'board', 'created_at']

admin.site.register(Postbookmark, PostbookmarkAdmin)
admin.site.register(Resumebookmark, ResumebookmarkAdmin)
admin.site.register(Boardbookmark, BoardbookmarkAdmin)