from rest_framework import serializers
from .models import User
from urllib.parse import urlparse
import requests


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = [
        #     "uid",
        #     "name",
        #     "email",
        #     "profile",
        #     "created_at",
        #     "is_active",
        # ]

        fields = "__all__"
