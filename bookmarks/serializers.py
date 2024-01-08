from rest_framework import serializers
from .models import Postbookmark,Resumebookmark,Boardbookmark

class PostFavoriteSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField('get_author_name')
    
    class Meta:
        model = Postbookmark
        fields = "__all__"
    
    def get_author_name(self, obj):
        return obj.author.displayName

class ResumeFavoriteSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField('get_author_name')

    class Meta:
        model = Resumebookmark
        fields = "__all__"

    def get_author_name(self, obj):
        return obj.author.displayName
    
class BoardFavoriteSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField('get_author_name')

    class Meta:
        model = Boardbookmark
        fields = "__all__"

    def get_author_name(self, obj):
        return obj.author.displayName