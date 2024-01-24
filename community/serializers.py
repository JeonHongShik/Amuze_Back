from rest_framework import serializers
from .models import Board, Comment

class CommentSerializer(serializers.ModelSerializer):
    # author_name = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = "__all__"

    # def get_author_name(self, obj):
    #     return obj.author.displayName  

class BoardSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    created_at = serializers.DateTimeField(source='created_date', format="%Y-%m-%d %H:%M")
    # author_name = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ['id', 'title', 'content', 'author', 'created_at', 'likes_count', 'comments_count']

    # def get_author_name(self, obj):
    #     return obj.author.displayName  
