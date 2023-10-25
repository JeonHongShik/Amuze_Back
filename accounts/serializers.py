<<<<<<< HEAD
from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
=======
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
>>>>>>> 449f363306bc1ffaec77f6392861278cbb95f3fa
