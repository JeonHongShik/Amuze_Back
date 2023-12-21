from django.contrib import admin
from .models import Resume, Education, Career, Award, Completion, Region, Image


class ResumeAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ("author", "gender", "age", "created_at", "updated_at")


class EducationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "education",
    )


class CareerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "career",
    )


class AwardAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "award",
    )


class CompletionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "completion",
    )


class RegionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "region",
    )


class ImageAdmin(admin.ModelAdmin):
    list_display = ("id", "image")


admin.site.register(Resume, ResumeAdmin)
admin.site.register(Education, EducationAdmin)
admin.site.register(Career, CareerAdmin)
admin.site.register(Award, AwardAdmin)
admin.site.register(Completion, CompletionAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Image, ImageAdmin)
