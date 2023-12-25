from django.urls import path
from .views import (
    PostBookmarkCreateView, 
    PostBookmarkDeleteView, 
    GetMyPostBookmarksView,
    BoardBookmarkCreateView,
    BoardBookmarkDeleteView,
    GetMyBoardBookmarksView,
    ResumeBookmarkCreateView,
    ResumeBookmarkDeleteView,
    GetMyResumeBookmarksView
)

urlpatterns = [
    path("bookmarks/post/", PostBookmarkCreateView.as_view(), name="post_bookmark_create"),
    path("bookmarks/post/<int:pk>", PostBookmarkDeleteView.as_view(), name="post_bookmark_delete"),
    path("bookmarks/post/my/", GetMyPostBookmarksView.as_view(), name="my_post_bookmarks"),
    path("bookmarks/board/", BoardBookmarkCreateView.as_view(), name="board_bookmark_create"),
    path("bookmarks/board/<int:pk>", BoardBookmarkDeleteView.as_view(), name="board_bookmark_delete"),
    path("bookmarks/board/my/", GetMyBoardBookmarksView.as_view(), name="my_board_bookmarks"),
    path("bookmarks/resume/", ResumeBookmarkCreateView.as_view(), name="resume_bookmark_create"),
    path("bookmarks/resume/<int:pk>", ResumeBookmarkDeleteView.as_view(), name="resume_bookmark_delete"),
    path("bookmarks/resume/my/", GetMyResumeBookmarksView.as_view(), name="my_resume_bookmarks"),
]
