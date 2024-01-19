from rest_framework import serializers
from .models import Post
from datetime import datetime


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField('get_author_name')

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'region', 'type', 'pay', 'deadline', 'datetime', 'introduce', 'wishtype','mainimage', 'otherimages1', 'otherimages2', 'otherimages3', 'otherimages4']

    # def get_author_name(self, obj):
    #     return obj.author.displayName  

    # def get_deadline(self, obj):
    #     if obj.deadline:
    #         if isinstance(obj.deadline, str):
    #             deadline = datetime.strptime(obj.deadline, '%Y-%m-%d %I:%M %p')
    #         else:
    #             deadline = obj.deadline
    #         return deadline.strftime('%Y-%m-%d %I:%M %p')
    #     else:
    #         return None

    # def get_datetime(self, obj):
    #     if obj.datetime:
    #         if isinstance(obj.datetime, str):
    #             datetime_obj = datetime.strptime(obj.datetime, '%Y-%m-%d %I:%M %p')
    #         else:
    #             datetime_obj = obj.datetime
    #         return datetime_obj.strftime('%Y-%m-%d %I:%M %p')
    #     else:
    #         return None
        
    # def to_internal_value(self, data):
    #     internal_value = super().to_internal_value(data)
    #     if isinstance(data.get('deadline'), str):
    #         internal_value['deadline'] = datetime.strptime(data.get('deadline'), '%Y-%m-%d %I:%M %p')
    #     if isinstance(data.get('datetime'), str):
    #         internal_value['datetime'] = datetime.strptime(data.get('datetime'), '%Y-%m-%d %I:%M %p')
    #     return internal_value