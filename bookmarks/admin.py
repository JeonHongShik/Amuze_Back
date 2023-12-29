from django.contrib import admin
from .models import Postbookmark,Resumebookmark,Boardbookmark

class PostbookmarkAdmin(admin.ModelAdmin):
    list_display = ["id",'author', 'post', 'created_at']
    list_filter = ["id",'author', 'post', 'created_at']


class ResumebookmarkAdmin(admin.ModelAdmin):
    list_display = ["id",'author', 'resume', 'created_at']
    list_filter = ["id",'author', 'resume', 'created_at']

class BoardbookmarkAdmin(admin.ModelAdmin):
    list_display = ["id",'author', 'board', 'created_at']
    list_filter = ["id",'author', 'board', 'created_at']

admin.site.register(Postbookmark, PostbookmarkAdmin)
admin.site.register(Resumebookmark, ResumebookmarkAdmin)
admin.site.register(Boardbookmark, BoardbookmarkAdmin)