from django.urls import path
from .views import BookmarkCreateView, BookmarkDeleteView,GetMyBookmarksView

urlpatterns = [
    path('bookmark/', BookmarkCreateView.as_view(), name='bookmark_create'),
    path('bookmark/<int:pk>', BookmarkDeleteView.as_view(), name='bookmark_delete'),
    path('mybookmark/',GetMyBookmarksView.as_view())
]
