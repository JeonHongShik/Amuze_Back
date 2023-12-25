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
            "phone",
            "gender",
            "age",
            "introduce",
            "image",
            "education",
            "career",
            "award",
            "region",
        ]

    def create(self, validated_data):
        education_data = validated_data.pop("education")
        career_data = validated_data.pop("career")
        award_data = validated_data.pop("award")
        region_data = validated_data.pop("region")

        resume = Resume.objects.create(**validated_data)

        for education in education_data:
            Education.objects.create(resume=resume, **education)

        for career in career_data:
            Career.objects.create(resume=resume, **career)

        for award in award_data:
            Award.objects.create(resume=resume, **award)

        for region in region_data:
            Region.objects.create(resume=resume, **region)

        return resume
