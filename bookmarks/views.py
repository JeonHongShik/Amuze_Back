# views.py

from django.http import JsonResponse
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Postbookmark,Resumebookmark,Boardbookmark
from .serializers import PostFavoriteSerializer,ResumeFavoriteSerializer,BoardFavoriteSerializer
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView


class ExceptionHandler:
    def handle_exception(self, exc):
        response = super().handle_exception(exc)
        response.data = {"error": str(exc)}
        response.status_code = status.HTTP_400_BAD_REQUEST
        return response



## Post
class PostBookmarkCreateView(ExceptionHandler, generics.ListCreateAPIView):
    queryset = Postbookmark.objects.all()
    serializer_class = PostFavoriteSerializer
    # permission_classes = [permissions.IsAuthenticated] 
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostBookmarkDeleteView(ExceptionHandler, generics.DestroyAPIView):
    queryset = Postbookmark.objects.all()
    serializer_class = PostFavoriteSerializer
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [AllowAny]

    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)

        if request.user != obj.user:
            self.permission_denied(request)


class GetMyPostBookmarksView(APIView):
    def get(self, request):
        posts = Postbookmark.objects.filter(user=request.user.uid)
        serializer = PostFavoriteSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)



## Resume
class ResumeBookmarkCreateView(ExceptionHandler, generics.ListCreateAPIView):
    queryset = Resumebookmark.objects.all()
    serializer_class = ResumeFavoriteSerializer
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ResumeBookmarkDeleteView(ExceptionHandler, generics.DestroyAPIView):
    queryset = Resumebookmark.objects.all()
    serializer_class = ResumeFavoriteSerializer
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [AllowAny]

    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)

        if request.user != obj.user:
            self.permission_denied(request)


class GetMyResumeBookmarksView(APIView):
    def get(self, request):
        posts = Resumebookmark.objects.filter(user=request.user.uid)
        serializer = ResumeFavoriteSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    


##Community
class BoardBookmarkCreateView(ExceptionHandler, generics.ListCreateAPIView):
    queryset = Boardbookmark.objects.all()
    serializer_class = BoardFavoriteSerializer
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BoardBookmarkDeleteView(ExceptionHandler, generics.DestroyAPIView):
    queryset = Boardbookmark.objects.all()
    serializer_class = BoardFavoriteSerializer
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [AllowAny]

    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)

        if request.user != obj.user:
            self.permission_denied(request)


class GetMyBoardBookmarksView(APIView):
    def get(self, request):
        posts = Boardbookmark.objects.filter(user=request.user.uid)
        serializer = BoardFavoriteSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)