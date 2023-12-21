# views.py

from django.http import JsonResponse
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import bookmark
from .serializers import FavoriteSerializer
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView


class ExceptionHandler:
    def handle_exception(self, exc):
        response = super().handle_exception(exc)
        response.data = {"error": str(exc)}
        response.status_code = status.HTTP_400_BAD_REQUEST
        return response


class BookmarkCreateView(ExceptionHandler, generics.ListCreateAPIView):  # 북마크생성
    queryset = bookmark.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]  # 인증된 사용자만 접근 가능
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # 즐겨찾기 추가는 요청한 사용자로 설정


class BookmarkDeleteView(ExceptionHandler, generics.DestroyAPIView):
    queryset = bookmark.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]  # 인증된 사용자만 접근 가능
    permission_classes = [AllowAny]

    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)

        if request.user != obj.user:  # 즐겨찾기 삭제는 해당 즐겨찾기를 추가한 사용자만 가능
            self.permission_denied(request)


class GetMyBookmarksView(APIView):
    def get(self, request):
        posts = bookmark.objects.filter(user=request.user.uid)
        serializer = FavoriteSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
