from rest_framework import serializers
from .models import Post, Image, wishtype

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"

class WishTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = wishtype
        fields = "__all__"

class PostSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    wish_types = WishTypeSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'region', 'concert_type', 'pay', 'deadline', 'datetime', 'introduce', 'wish_types', 'images']
