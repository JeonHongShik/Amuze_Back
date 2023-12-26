from django.contrib import admin
from .models import Board, Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ("board", "writer", "created_date")
    search_fields = ("board__title", "writer__username")
    list_filter = ("created_date", "writer")


class BoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'writer', 'created_date', 'like_count')
    list_filter = ('writer', 'created_date')
    ordering = ('-created_date',)


admin.site.register(Board, BoardAdmin)
admin.site.register(Comment, CommentAdmin)
