from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from django.http import JsonResponse
from django.db import transaction


class BaseUserView(APIView):
    permission_classes = [AllowAny]

    def get_user(self, Uidd):
        return get_object_or_404(User, Uidd=Uidd)


class PostListView(BaseUserView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class PostDetailView(RetrieveAPIView):  # 특정 유저 정보 보기
    queryset = Post.objects.all()
    serializer_class = PostSerializer