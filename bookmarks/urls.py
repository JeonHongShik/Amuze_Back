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
    #post
    path("bookmark/post/", PostBookmarkCreateView.as_view(), name="post_bookmark_create"),
    path("bookmark/post/delete/<int:pk>/", PostBookmarkDeleteView.as_view(), name="post_bookmark_delete"),
    path("bookmark/mypost/<str:uid>/", GetMyPostBookmarksView.as_view(), name="my_post_bookmarks"),
    #community
    path("bookmark/board/", BoardBookmarkCreateView.as_view(), name="board_bookmark_create"),
    path("bookmark/board/delete/<int:pk>/", BoardBookmarkDeleteView.as_view(), name="board_bookmark_delete"),
    path("bookmark/myboard/<str:uid>/", GetMyBoardBookmarksView.as_view(), name="my_board_bookmarks"),
    #resume
    path("bookmark/resume/", ResumeBookmarkCreateView.as_view(), name="resume_bookmark_create"),
    path("bookmark/resume/delete/<int:pk>/", ResumeBookmarkDeleteView.as_view(), name="resume_bookmark_delete"),
    path("bookmark/myresume/<str:uid>/", GetMyResumeBookmarksView.as_view(), name="my_resume_bookmarks"),
]
