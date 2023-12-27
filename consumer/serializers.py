from rest_framework import serializers
from .models import Resume, Education, Career, Award, Region


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = "__all__"


class CareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Career
        fields = "__all__"


class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = "__all__"


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = "__all__"


class ResumeSerializer(serializers.ModelSerializer):
    education = EducationSerializer(many=True)
    career = CareerSerializer(many=True)
    award = AwardSerializer(many=True)
    region = RegionSerializer(many=True)

    class Meta:
        model = Resume
        fields = [
            "author",
            "gender",
            "age",
            "introduce",
            "photo",
            "education",
            "career",
            "award",
            "region",
        ]