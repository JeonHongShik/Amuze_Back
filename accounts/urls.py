from django.urls import path
from .views import accountsViews, UserListView, UpdateDeleteUserView

urlpatterns = [
    path("CreateUser/", accountsViews.as_view()),
    path("Users/", UserListView.as_view()),
    path("User/detail/<str:pk>/", UserListView.as_view()),
    path("User/patch/<str:pk>/", UpdateDeleteUserView.as_view()),
    path("User/delete/<str:pk>/", UpdateDeleteUserView.as_view()),
]
