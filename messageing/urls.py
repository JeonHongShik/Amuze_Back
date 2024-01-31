from django.urls import path,include
from messageing import views
from messageing.views import mynotificationsviews,NotificationDeleteView

urlpatterns = [
    path('send_message/<str:uid>/', views.send_to_firebase_cloud_messaging),
    path('mynotification/<str:uid>/', mynotificationsviews.as_view()),
    path('notifications/<int:pk>/delete/', NotificationDeleteView.as_view()),
    path('send_alarm_Users/' ,views.send_to_all_user_notifications),
]