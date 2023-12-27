from django.urls import path
from .views import (
    accountsViews,
    UserListView,
    UpdateUserView,
    DeleteUserView,
    UserDetailView,
    syncdbfirebase,
)

urlpatterns = [
    path("CreateUser/", accountsViews.as_view()),
    path("syncdb/", syncdbfirebase.as_view()), # get,post 둘다됨
    path("Users/", UserListView.as_view()),
    path("User/detail/<int:pk>/", UserDetailView.as_view()),
    path("User/patch/<int:pk>/", UpdateUserView.as_view()),
    path("User/delete/<int:pk>/", DeleteUserView.as_view()),
]
