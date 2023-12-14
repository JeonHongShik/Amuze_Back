from django.contrib import admin
from .models import Resume, Education, Experience, Award, Completion, Place


class ResumeAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ("author", "gender", "age", "created_at", "updated_at")


class EducationAdmin(admin.ModelAdmin):
    list_display = ("id","education",)


class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("id","experience",)


class AwardAdmin(admin.ModelAdmin):
    list_display = ("id","award",)


class CompletionAdmin(admin.ModelAdmin):
    list_display = ("id","completion",)


class PlaceAdmin(admin.ModelAdmin):
    list_display = ("id","place",)


admin.site.register(Resume, ResumeAdmin)
admin.site.register(Education, EducationAdmin)
admin.site.register(Experience, ExperienceAdmin)
admin.site.register(Award, AwardAdmin)
admin.site.register(Completion, CompletionAdmin)
admin.site.register(Place, PlaceAdmin)
