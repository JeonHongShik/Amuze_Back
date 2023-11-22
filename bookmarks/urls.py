from django.urls import path
from .views import FavoriteListCreateView, FavoriteDeleteView

urlpatterns = [
    path('bookmark/', FavoriteListCreateView.as_view(), name='favorite_list_create'),
    path('bookmark/<int:pk>', FavoriteDeleteView.as_view(), name='favorite_delete'),
]
