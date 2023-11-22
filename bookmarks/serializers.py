from rest_framework import serializers
from .models import bookmark

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = bookmark
        fields = ['user', 'post', 'created_at']