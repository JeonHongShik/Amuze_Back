from rest_framework import serializers
from .models import consumer


class ConsumerSerializer(serializers.ModelSerializer):
    class Meta:
        model = consumer
        fields = "__all__"
        

