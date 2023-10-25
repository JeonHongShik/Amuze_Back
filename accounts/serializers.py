from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "kakaoid",
            "name",
            "profile",
            "created_at",
            "is_active",
            "is_staff",
        ]
        # fields = "__all__"