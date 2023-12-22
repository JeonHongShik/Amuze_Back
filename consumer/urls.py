from django.urls import path
from .views import ResumeListView, GetMyResumeView, ResumeDetailView, ResumeCreateView

urlpatterns = [
    path("resume/", ResumeListView.as_view()),
    path("resume/<int:pk>/", ResumeDetailView.as_view()),
]
