from django.urls import path
from .views import WriteConsumerView,ConsumerListView


urlpatterns = [
    path('ConsumerView/',ConsumerListView.as_view()),
    path('WriteConsumer/',WriteConsumerView.as_view()),
]
