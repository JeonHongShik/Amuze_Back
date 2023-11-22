from rest_framework import serializers
from .models import Favorite, Post, User

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['user', 'post', 'created_at']