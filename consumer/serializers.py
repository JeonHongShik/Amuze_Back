from rest_framework import serializers
from .models import Resume, Education, Career, Award, Completion, Region

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'

class CareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Career
        fields = '__all__'

class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = '__all__'

class CompletionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Completion
        fields = '__all__'

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'

class ResumeSerializer(serializers.ModelSerializer):
    education = EducationSerializer(many=True)
    career = CareerSerializer(many=True)
    award = AwardSerializer(many=True)
    completion = CompletionSerializer(many=True)
    place = RegionSerializer(many=True)

    class Meta:
        model = Resume
        fields = ['author', 'phone', 'gender', 'age', 'introduce', 'image', 'education', 'career', 'award', 'completion', 'Region']

    def create(self, validated_data):
        education_data = validated_data.pop('education')
        career_data = validated_data.pop('career')
        award_data = validated_data.pop('award')
        completion_data = validated_data.pop('completion')
        Region_data = validated_data.pop('Region')

        resume = Resume.objects.create(**validated_data)

        for education in education_data:
            Education.objects.create(resume=resume, **education)

        for career in career_data:
            Career.objects.create(resume=resume, **career)

        for award in award_data:
            Award.objects.create(resume=resume, **award)

        for completion in completion_data:
            Completion.objects.create(resume=resume, **completion)

        for Region in Region_data:
            Region.objects.create(resume=resume, **Region)

        return resume
