from django.urls import path
from .views import (
    accountsViews,
    UserListView,
    UpdateUserView,
    DeleteUserView,
    UserDetailView,
)

urlpatterns = [
    path("CreateUser/", accountsViews.as_view()),
    path("Users/", UserListView.as_view()),
    path("User/detail/<str:pk>/", UserDetailView.as_view()),
    path("User/patch/<str:pk>/", UpdateUserView.as_view()),
    path("User/delete/<str:pk>/", DeleteUserView.as_view()),
]
