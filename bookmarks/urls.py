from django.urls import path
from .views import (PostBookmarkCreateView,PostBookmarkDeleteView,GetMyPostBookmarksView,
                    BoardBookmarkCreateView,BoardBookmarkDeleteView,GetMyBoardBookmarksView,ResumeBookmarkCreateView,
                    ResumeBookmarkDeleteView, GetMyResumeBookmarksView,CheckPostBookmarkView,CheckResumeBookmarkView,
                    CheckBoardBookmarkView)

urlpatterns = [
    #post
    path("bookmark/post/", PostBookmarkCreateView.as_view(), name="post_bookmark_create"),
    path("bookmark/post/delete/<int:pk>/", PostBookmarkDeleteView.as_view(), name="post_bookmark_delete"),
    path("bookmark/mypost/<str:uid>/", GetMyPostBookmarksView.as_view(), name="my_post_bookmarks"),
    path("bookmark/post/check/<str:uid>/<int:post_id>/", CheckPostBookmarkView.as_view(), name="check_post"),
    #community
    path("bookmark/board/", BoardBookmarkCreateView.as_view(), name="board_bookmark_create"),
    path("bookmark/board/delete/<int:pk>/", BoardBookmarkDeleteView.as_view(), name="board_bookmark_delete"),
    path("bookmark/myboard/<str:uid>/", GetMyBoardBookmarksView.as_view(), name="my_board_bookmarks"),
    path("bookmark/board/check/<str:uid>/<int:board_id>/", CheckBoardBookmarkView.as_view(), name="check_board"),
    
    #resume
    path("bookmark/resume/", ResumeBookmarkCreateView.as_view(), name="resume_bookmark_create"),
    path("bookmark/resume/delete/<int:pk>/", ResumeBookmarkDeleteView.as_view(), name="resume_bookmark_delete"),
    path("bookmark/myresume/<str:uid>/", GetMyResumeBookmarksView.as_view(), name="my_resume_bookmarks"),
    path("bookmark/resume/check/<str:uid>/<int:resume_id>/", CheckResumeBookmarkView.as_view(), name="check_resume"),
]