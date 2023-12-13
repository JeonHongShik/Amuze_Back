from rest_framework import serializers
from .models import Board, Comment, Reply


class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    replies = ReplySerializer(many=True)

    class Meta:
        model = Comment
        fields = "__all__"


class BoardSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)

    class Meta:
        model = Board
        fields = "__all__"
