from rest_framework import serializers
from .models import consumer


class ConsumerSerializer(serializers.ModelSerializer):
    class Meta:
        model = consumer
        fields = [
            "id",
            "kakaoid",
            "name",
            "get_image",
            "created_at",
            "is_active",
        ]
        # fields = "__all__"
        

