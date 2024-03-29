from django.urls import path
from .views import CommunitylistView, CreatecommunityView,UpdatecommunityView,CommunityDeleteView,MyCommunityView,CommunityDetailView
from .views import CommentlistView,CommentCreateView,commentupdateeview,commentdeleteview
from .views import AddLikeView

urlpatterns = [
    #community
    path("community/", CommunitylistView.as_view()),
    path("mycommunity/<str:uid>", MyCommunityView.as_view()),
    path("community/detail/<int:pk>/", CommunityDetailView.as_view()),
    path("community/create/", CreatecommunityView.as_view()),
    path("community/patch/<int:pk>/",UpdatecommunityView.as_view()),
    path("community/delete/<int:pk>/",CommunityDeleteView.as_view()),
    #comment
    path("comment/",CommentlistView.as_view()),
    path("comment/create/",CommentCreateView.as_view()),
    path("comment/patch/<int:pk>/",commentupdateeview.as_view()),
    path("comment/delete/<int:pk>/",commentdeleteview.as_view()),
    #add like
    path("like_add_count/<int:pk>/",AddLikeView.as_view()),
]
