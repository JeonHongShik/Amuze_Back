from rest_framework import serializers
from messageing.models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    
    
    class Meta:
        model = Notification
        fields = ['id','uid', 'title','messagebody','content', 'board_id', 'created_at']

    def get_title(self, obj):
        return obj.title.title