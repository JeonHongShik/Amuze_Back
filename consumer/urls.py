from django.urls import path
from .views import ResumeListCreateView, ResumeRetrieveUpdateDestroyView

urlpatterns = [
    path("resumes/", ResumeListCreateView.as_view(), name="resume-list-create"),
    path(
        "resumes/<int:pk>/",
        ResumeRetrieveUpdateDestroyView.as_view(),
        name="resume-retrieve-update-destroy",
    ),
]
