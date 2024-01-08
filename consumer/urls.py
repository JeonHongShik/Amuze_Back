from django.urls import path
from .views import (
    ResumeListView,
    GetMyResumeView,
    ResumeDetailView,
    ResumeCreateView,
    ResumeUpdateView,
    ResumeDeleteView,
)

urlpatterns = [
    path("resume/", ResumeListView.as_view(), name="resume-list"),
    path("myresume/<str:uid>/", GetMyResumeView.as_view(), name="my-resume"),
    path("resume/<int:pk>/", ResumeDetailView.as_view(), name="resume-detail"),
    path("resume/create/", ResumeCreateView.as_view(), name="resume-create"),
    path("resume/patch/<int:pk>/", ResumeUpdateView.as_view(), name="resume-update"),
    path("resume/delete/<int:pk>/", ResumeDeleteView.as_view(), name="resume-delete"),
]
