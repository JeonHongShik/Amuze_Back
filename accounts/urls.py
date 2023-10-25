from django.urls import path
from .views import UserListView, KakaoLoginCallbackView ,UserDetailsView,UpdateDeleteUserView

urlpatterns = [
    path('users/', UserListView.as_view()),
    path('users/detail/<str:kakaoid>/', UserDetailsView.as_view()),
    path('users/delete/<str:kakaoid>/', UpdateDeleteUserView.as_view()),
    path('users/update/<str:kakaoid>/', UpdateDeleteUserView.as_view()),
    path('kakao-login/', KakaoLoginCallbackView.as_view()),
]
