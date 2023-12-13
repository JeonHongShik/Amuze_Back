from django.contrib import admin
from .models import Resume


class ResumeAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = (
        "name",
        "phone_number",
        "gender",
        "age",
        "education",
        "experience",
        "award",
        "introduce",
        "created_at",
        "updated_at",
        "photo",
    )


admin.site.register(Resume, ResumeAdmin)
