from django.urls import path
from .views import (
    # localsignupview,
    UserListView,
    UpdateUserView,
    DeleteUserView,
    UserDetailView,
    syncdbfirebase,
    signupfirebaseview,
)

urlpatterns = [
    # path("CreateUser/", localsignupview.as_view()),
    path("SignUp/", signupfirebaseview.as_view()),
    path("syncdb/", syncdbfirebase.as_view()),
    path("Users/", UserListView.as_view()),
    path("User/detail/<int:pk>/", UserDetailView.as_view()),
    path("User/patch/<int:pk>/", UpdateUserView.as_view()),
    path("User/delete/<int:pk>/", DeleteUserView.as_view()),
]
