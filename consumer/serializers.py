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
        education_data = validated_data.pop('education')
        career_data = validated_data.pop('career')
        award_data = validated_data.pop('award')
        region_data = validated_data.pop('region')

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

    def update(self, instance, validated_data):
        instance.author = validated_data.get('author', instance.author)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.age = validated_data.get('age', instance.age)
        instance.introduce = validated_data.get('introduce', instance.introduce)
        instance.image = validated_data.get('image', instance.image)
        instance.save()

        education = validated_data.get('education')

        if education:
            Education.objects.filter(resume=instance).delete()
            for education in education:
                Education.objects.create(resume=instance, **education)

        career = validated_data.get('career')

        if career:
            Career.objects.filter(resume=instance).delete()
            for career in career:
                Career.objects.create(resume=instance, **career)

        award = validated_data.get('award')

        if award:
            Award.objects.filter(resume=instance).delete()
            for award in award:
                Award.objects.create(resume=instance, **award)

        region = validated_data.get('region')

        if region:
            Region.objects.filter(resume=instance).delete()
            for region in region:
                Region.objects.create(resume=instance, **region)

        return instance
