from django.urls import path
from .views import PostListView

urlpatterns = [
    path("post/", PostListView.as_view(), name="post_list"),
]
