from rest_framework import serializers
from messageing.models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id','uid', 'title', 'content', 'board_id', 'created_at']
