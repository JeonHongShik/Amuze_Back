from django.urls import path
from .views import PostListView, PostDetailView,GetMyPostView,PostCreateView

urlpatterns = [
    path('postview/', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('mypost/', GetMyPostView.as_view()),
    path('createpost/', PostCreateView.as_view()),
]
