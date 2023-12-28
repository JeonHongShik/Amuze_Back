from django.contrib import admin
from .models import Resume, Education, Career, Award, Region


class ResumeAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = (
        "author",
        "title",
        "gender",
        "age",
        "regions_list",
        "educations_list",
        "careers_list",
        "awards_list",
        "introduce",
        "created_at",
        "updated_at",
    )

    def regions_list(self, obj):
        return ", ".join([str(region) for region in obj.regions.all()])

    def educations_list(self, obj):
        return ", ".join([str(education) for education in obj.educations.all()])

    def careers_list(self, obj):
        return ", ".join([str(career) for career in obj.careers.all()])

    def awards_list(self, obj):
        return ", ".join([str(award) for award in obj.awards.all()])


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


class RegionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "region",
    )


class ImageAdmin(admin.ModelAdmin):
    list_display = ("id",)


admin.site.register(Resume, ResumeAdmin)
admin.site.register(Education, EducationAdmin)
admin.site.register(Career, CareerAdmin)
admin.site.register(Award, AwardAdmin)
admin.site.register(Region, RegionAdmin)
