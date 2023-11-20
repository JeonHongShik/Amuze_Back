from rest_framework import serializers
from .models import User
from urllib.parse import urlparse
import requests


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = [
        #     "Uidd",
        #     "name",
        #     "email",
        #     "profile",
        #     "created_at",
        #     "is_active",
        # ]
        fields = "__all__"

    def validate_profile(self, value):
        parsed = urlparse(value)
        if bool(parsed.netloc) and bool(parsed.scheme):
            response = requests.head(value)
            content_type = response.headers["content-type"]
            if "profile" not in content_type:
                raise serializers.ValidationError("URL이 이미지 파일이 아닙니다.")
            else:
                raise serializers.ValidationError("URL 형식이 아닙니다.")

        return value
