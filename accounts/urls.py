<<<<<<< HEAD
from django.urls import include, path
from . import views


urlpatterns = [
    # path("")
    # path("", views.UserListView.as_view()),  # 유저 리스트 읽기
]
=======
from django.urls import path
from .views import UserListView, KakaoLoginCallbackView ,UserDetailsView,UpdateDeleteUserView

urlpatterns = [
    path('users/', UserListView.as_view()),
    path('users/detail/<str:kakaoid>/', UserDetailsView.as_view()),
    path('users/delete/<str:kakaoid>/', UpdateDeleteUserView.as_view()),
    path('users/update/<str:kakaoid>/', UpdateDeleteUserView.as_view()),
    path('kakao-login/', KakaoLoginCallbackView.as_view()),
]
>>>>>>> 449f363306bc1ffaec77f6392861278cbb95f3fa
