from django.contrib import admin
from .models import User, Post, Favorite

class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']
    list_filter = ['user', 'post', 'created_at']
    search_fields = ['user__name', 'post__title']

admin.site.register(Favorite, FavoriteAdmin)
