from rest_framework import serializers
from .models import Post



class PostSerializer(serializers.ModelSerializer):
    # mainimage = serializers.ImageField(max_length=None, use_url=True)
    # otherimages1 = serializers.ImageField(max_length=None, use_url=True)
    # otherimages2 = serializers.ImageField(max_length=None, use_url=True)
    # otherimages3 = serializers.ImageField(max_length=None, use_url=True)
    # otherimages4 = serializers.ImageField(max_length=None, use_url=True)
    author = serializers.SerializerMethodField('get_author_name')

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'region', 'type', 'pay', 'deadline', 'datetime', 'introduce', 'wishtype', 'mainimage', 'otherimages1', 'otherimages2', 'otherimages3', 'otherimages4']

    def get_author_name(self, obj):
        return obj.author.displayName  