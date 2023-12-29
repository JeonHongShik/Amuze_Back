from rest_framework import serializers
from .models import Resume, Education, Career, Award, Region


class EducationSerializer(serializers.ModelSerializer):
    education = serializers.CharField()

    class Meta:
        model = Education
        fields = ["id", "education", "resume"]

class CareerSerializer(serializers.ModelSerializer):
    career = serializers.CharField()

    class Meta:
        model = Career
        fields = ["id", "career", "resume"]

class AwardSerializer(serializers.ModelSerializer):
    award = serializers.CharField()

    class Meta:
        model = Award
        fields = ["id", "award", "resume"]

class RegionSerializer(serializers.ModelSerializer):
    region = serializers.CharField()

    class Meta:
        model = Region
        fields = ["id", "region", "resume"]


class ResumeSerializer(serializers.ModelSerializer):
    educations = EducationSerializer(many=True)
    careers = CareerSerializer(many=True)
    awards = AwardSerializer(many=True)
    regions = RegionSerializer(many=True)
    # mainimage = serializers.ImageField(max_length=None, use_url=True)
    # otherimages1 = serializers.ImageField(max_length=None, use_url=True)
    # otherimages2 = serializers.ImageField(max_length=None, use_url=True)
    # otherimages3 = serializers.ImageField(max_length=None, use_url=True)
    # otherimages4 = serializers.ImageField(max_length=None, use_url=True)
    author = serializers.SerializerMethodField('get_author_name')

    class Meta:
        model = Resume
        fields = [
            "id",
            "title",
            "author",
            "gender",
            "age",
            "introduce",
            "educations",
            "careers",
            "awards",
            "regions",
            "mainimage", 
            "otherimages1", 
            "otherimages2", 
            "otherimages3", 
            "otherimages4",
        ]

    def get_author_name(self, obj):
        return obj.author.displayName