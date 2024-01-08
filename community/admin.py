from django.contrib import admin
from .models import Board, Comment


class BoardAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "content","author")


class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "board", "author","content")


admin.site.register(Board, BoardAdmin)
admin.site.register(Comment, CommentAdmin)
