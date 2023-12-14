from django.contrib import admin
from .models import Board, Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ("board", "writer", "created_date")
    search_fields = ("board__title", "writer__username")
    list_filter = ("created_date", "writer")


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ("title", "writer", "registered_date", "like_count")
    search_fields = ("title", "writer__username")
    list_filter = ("registered_date", "writer")
    ordering = ("-registered_date",)


admin.site.register(Comment, CommentAdmin)
