from django.utils.html import format_html
from django.contrib import admin
from .models import User


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ["uid", "displayName", "email", "photoURL", "created_at", "is_active"]
    list_display_links = ["uid"]
    list_per_page = 10

    # def get_image(self, obj):
    #     if obj.profile and obj.profile.url:  # 'profile' 필드에 이미지 파일이 있는지 확인
    #         return format_html(
    #             '<img src="{}" width="50" height="50" />', obj.profile.url
    #         )
    #     else:
    #         return "이미지 없음"  # 이미지 파일이 없을 경우의 처리

    # get_image.short_description = "profile"


admin.site.register(User, UserAdmin)