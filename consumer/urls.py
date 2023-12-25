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
    path("resume/my/", GetMyResumeView.as_view(), name="my-resume"),
    path("resume/<int:pk>/", ResumeDetailView.as_view(), name="resume-detail"),
    path("resume/create/", ResumeCreateView.as_view(), name="resume-create"),
    path("resume/<int:pk>/update/", ResumeUpdateView.as_view(), name="resume-update"),
    path("resume/<int:pk>/delete/", ResumeDeleteView.as_view(), name="resume-delete"),
]
