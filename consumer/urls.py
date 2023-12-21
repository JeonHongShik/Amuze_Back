from django.urls import path
from .views import ResumeListView,GetMyResumeView,ResumeDetailView,ResumeCreateView

urlpatterns = [
    path('resumeview/', ResumeListView.as_view()),
    path('myresume/', GetMyResumeView.as_view()),
    path('createresume/', ResumeCreateView.as_view()),
    path('resume/<int:pk>/', ResumeDetailView.as_view()),
]
