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
    path("User/detail/<int:pk>/", UserDetailView.as_view()),
    path("User/patch/<int:pk>/", UpdateUserView.as_view()),
    path("User/delete/<int:pk>/", DeleteUserView.as_view()),
]
