from django.urls import path,include
from . import views

urlpatterns = [
    path('send_message/<str:uid>/', views.send_to_firebase_cloud_messaging),
]