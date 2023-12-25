from rest_framework import serializers
from .models import Postbookmark,Resumebookmark,Boardbookmark

class PostFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Postbookmark
        fields = "__all__"


class ResumeFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resumebookmark
        fields = "__all__"

class BoardFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boardbookmark
        fields = "__all__"