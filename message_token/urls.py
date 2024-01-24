from django.urls import path,include
from . import views
from .views import mynotificationsviews

urlpatterns = [
    path('send_message/<str:uid>/', views.send_to_firebase_cloud_messaging),
    path('mynotification/<str:uid>/', mynotificationsviews.as_view()),
    # path('delete_notification/<str:uid>/', DeleteNotificationView.as_view()),
]