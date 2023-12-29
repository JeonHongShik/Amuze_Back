from django.urls import path
from .views import (
    # localsignupview,
    UserListView,
    UpdateUserView,
    DeleteUserView,
    UserDetailView,
    syncdbfirebase,
    SignupFirebaseView,
)

urlpatterns = [
    # path("CreateUser/", localsignupview.as_view()),
    path("SignUp/", SignupFirebaseView.as_view()),
    path("syncdb/", syncdbfirebase.as_view()),
    path("Users/", UserListView.as_view()),
    path("User/detail/<str:uid>/", UserDetailView.as_view()),
    path("User/patch/<str:uid>/", UpdateUserView.as_view()),
    path("User/delete/<str:uid>/", DeleteUserView.as_view()),
]