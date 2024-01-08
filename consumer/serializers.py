from rest_framework import serializers
from .models import Resume, Education, Career, Award, Completion, Region


class EducationSerializer(serializers.ModelSerializer):
    education = serializers.CharField()

    class Meta:
        model = Education
        fields = ["education"]


class CareerSerializer(serializers.ModelSerializer):
    career = serializers.CharField()

    class Meta:
        model = Career
        fields = ["career"]


class AwardSerializer(serializers.ModelSerializer):
    award = serializers.CharField()

    class Meta:
        model = Award
        fields = ["award"]


class CompletionSerializer(serializers.ModelSerializer):
    completion = serializers.CharField()

    class Meta:
        model = Completion
        fields = ["completion"]


class RegionSerializer(serializers.ModelSerializer):
    region = serializers.CharField()

    class Meta:
        model = Region
        fields = ["region"]


class ResumeSerializer(serializers.ModelSerializer):
    educations = EducationSerializer(many=True)
    careers = CareerSerializer(many=True)
    awards = AwardSerializer(many=True)
    completions = CompletionSerializer(many=True)
    regions = RegionSerializer(many=True)

    author = serializers.SerializerMethodField("get_author_name")

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
            "completions",
            "regions",
            "mainimage",
            "otherimages1",
            "otherimages2",
            "otherimages3",
            "otherimages4",
        ]

    def get_author_name(self, obj):
        return obj.author.displayName