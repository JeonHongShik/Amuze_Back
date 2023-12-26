from rest_framework import generics
from rest_framework.response import Response
from .models import Board, Comment
from .serializers import (
    BoardSerializer,
    CommentSerializer,
)


class BoardListAPIView(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer


class BoardRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer


class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
