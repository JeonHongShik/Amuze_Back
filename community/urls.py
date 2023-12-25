from django.urls import path
from .views import BoardListAPIView, BoardRetrieveUpdateDestroyAPIView

app_name = "community"

urlpatterns = [
    path("boards/", BoardListAPIView.as_view(), name="board-list"),
    path(
        "boards/<int:pk>/",
        BoardRetrieveUpdateDestroyAPIView.as_view(),
        name="board-detail",
    ),
]
