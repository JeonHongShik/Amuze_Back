from django.urls import path
from .views import PostListView, PostDetailView,GetMyPostView,PostCreateView,PostUpdateView,PostDeleteView

urlpatterns = [
    
    path('postview/', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('mypost/', GetMyPostView.as_view(), name='post_mypost'),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
]
