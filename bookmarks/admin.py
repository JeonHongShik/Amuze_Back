from django.contrib import admin
from .models import Postbookmark,Resumebookmark,Boardbookmark

class PostbookmarkAdmin(admin.ModelAdmin):
    list_display = ["id",'author', 'post']
    list_filter = ["id",'author', 'post']


class ResumebookmarkAdmin(admin.ModelAdmin):
    list_display = ["id",'author', 'resume']
    list_filter = ["id",'author', 'resume']

class BoardbookmarkAdmin(admin.ModelAdmin):
    list_display = ["id",'author', 'board']
    list_filter = ["id",'author', 'board']

admin.site.register(Postbookmark, PostbookmarkAdmin)
admin.site.register(Resumebookmark, ResumebookmarkAdmin)
admin.site.register(Boardbookmark, BoardbookmarkAdmin)