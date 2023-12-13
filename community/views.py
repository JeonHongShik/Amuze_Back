from rest_framework import generics
from rest_framework.response import Response
from .models import Board, Comment, Reply
from .serializers import (
    BoardSerializer,
    CommentSerializer,
    ReplySerializer,
)


class BoardListAPIView(generics.ListAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer


class BoardRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class ReplyCreateAPIView(generics.CreateAPIView):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
