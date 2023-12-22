from django.urls import path
from .views import BookmarkCreateView, BookmarkDeleteView, GetMyBookmarksView

urlpatterns = [
    path("bookmarks/", BookmarkCreateView.as_view(), name="bookmark_create"),
    path("bookmarks/<int:pk>", BookmarkDeleteView.as_view(), name="bookmark_delete"),
    path("bookmarks/my/", GetMyBookmarksView.as_view()),
]
