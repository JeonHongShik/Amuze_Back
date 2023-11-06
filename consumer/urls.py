from django.urls import path
from .views import WriteConsumerView, ConsumerListView, ConsumerDetailView


urlpatterns = [
    path("WriteConsumer/", WriteConsumerView.as_view()),
    path("ConsumerView/", ConsumerListView.as_view()),
    path("ConsumerView/<int:pk>", ConsumerDetailView.as_view()),
]
