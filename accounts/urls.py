from django.urls import path
from .views import accountsViews, UserListView, UserDetailsView

# from .views import UserListView, SignupView, UserDetailsView

urlpatterns = [
    path("CreateUser/", accountsViews.as_view()),
    path("Users/", UserListView.as_view()),
    path("User/detail/<str:pk>/", UserDetailsView.as_view()),
]
