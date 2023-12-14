from rest_framework import serializers
from .models import Board, Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class BoardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Board
        fields = "__all__"
