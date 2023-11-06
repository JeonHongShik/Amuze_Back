from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = [
        #     "Uidd",
        #     "name",
        #     "get_image",
        #     "created_at",
        #     "is_active",
        # ]
        fields = "__all__"
