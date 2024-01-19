from rest_framework import serializers
from .models import Board, Comment

class CommentSerializer(serializers.ModelSerializer):
    # author = serializers.SerializerMethodField('get_author_name')
    class Meta:
        model = Comment
        fields = "__all__"

    # def get_author_name(self, obj):
    #     return obj.author.displayName  

class BoardSerializer(serializers.ModelSerializer):
    # author = serializers.SerializerMethodField('get_author_name')
    class Meta:
        model = Board
        fields = "__all__"
        
    # def get_author_name(self, obj):
    #     return obj.author.displayName  