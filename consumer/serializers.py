from rest_framework import serializers
from .models import Resume, Education, Career, Award, Region


class EducationSerializer(serializers.ModelSerializer):
    education = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Education
        fields = ["id", "education", "resume"]

class CareerSerializer(serializers.ModelSerializer):
    career = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Career
        fields = ["id", "career", "resume"]

class AwardSerializer(serializers.ModelSerializer):
    award = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Award
        fields = ["id", "award", "resume"]

class RegionSerializer(serializers.ModelSerializer):
    region = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Region
        fields = ["id", "region", "resume"]


class ResumeSerializer(serializers.ModelSerializer):
    educations = EducationSerializer(many=True)
    careers = CareerSerializer(many=True)
    awards = AwardSerializer(many=True)
    regions = RegionSerializer(many=True)

    class Meta:
        model = Resume
        fields = [
            "id",
            "author",
            "gender",
            "age",
            "introduce",
            "educations",
            "careers",
            "awards",
            "regions",
        ]