from django.urls import path
from .views import PostListView, PostDetailView,GetMyPostView,PostCreateView,PostUpdateView,PostDeleteView

urlpatterns = [
    
    path('postview/', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('mypost/<str:uid>/', GetMyPostView.as_view()),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('post/patch/<int:pk>/', PostUpdateView.as_view(), name='post_update'),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name='post_delete'),
]
