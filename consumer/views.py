from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import generics, status
from .models import Award, Education, Career, Region, Resume,Image
from .serializers import ResumeSerializer
from rest_framework.exceptions import ValidationError
from django.db import transaction

class BaseUserView(APIView):
    permission_classes = [AllowAny]

    # permission_classes = [permissions.IsAuthenticated]
    def get_user(self, uid):
        return get_object_or_404(User, uid=uid)


class ResumeListView(generics.ListAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer


class GetMyResumeView(BaseUserView):
    def get(self, request):
        try:
            posts = Resume.objects.filter(author=request.user.uid)
        except Resume.DoesNotExist:
            return JsonResponse(
                {"error": "정보를 찾을 수 없습니다"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = ResumeSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)


class ResumeDetailView(BaseUserView):
    def get_object(self, pk):
        try:
            return Resume.objects.get(pk=pk)
        except Resume.DoesNotExist:
            return None

    def get(self, request, pk):
        post_user = self.get_object(pk)
        if not post_user:
            return JsonResponse(
                {"error": "정보를 찾을 수 없습니다"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = ResumeSerializer(post_user)
        return JsonResponse(serializer.data, safe=False)


class ResumeCreateView(BaseUserView):
    @transaction.atomic
    def post(self, request):
        try:
            lst = request.data
            author = lst.get("author")
            title = lst.get("title")
            gender = lst.get("gender")
            age = lst.get("age")
            educations_data = lst.get("education")
            careers_data = lst.get("career")
            awards_data = lst.get("award")
            introduce = lst.get("introduce")
            regions_data = lst.get("region")
            photos = lst.get("image")

            print(lst)

            if (
                not author
                or not title
                or not gender
                or not age
                or not introduce
                or not regions_data
            ):
                raise ValidationError("필수 정보가 누락되었습니다")

            resume = Resume.objects.create(
                author=request.user.uid,
                title=title,
                gender=gender,
                age=age,
                educations_data=educations_data,
                careers_data=careers_data,
                awards_data=awards_data,
                introduce=introduce,
                regions_data=regions_data,
            )

            Education.objects.bulk_create(
                [Education(education=education, resume=resume) for education in educations_data]
            )

            Career.objects.bulk_create(
                [Career(career=career, resume=resume) for career in careers_data]
            )

            Award.objects.bulk_create(
                [Award(award=award, resume=resume) for award in awards_data]
            )

            Region.objects.bulk_create(
                [Region(region=region, resume=resume) for region in regions_data]
            )

            for photo in photos:
                Image.objects.create(photo=photo, resume=resume)

            serializer = ResumeSerializer(resume)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ResumeUpdateView(BaseUserView):
    @transaction.atomic
    def put(self, request, pk):
        try:
            resume = self.get_object(pk)
            if not resume:
                return JsonResponse(
                    {"error": "Resume not found."}, status=status.HTTP_404_NOT_FOUND
                )

            lst = request.data
            author = lst.get("author")
            title = lst.get("title")
            gender = lst.get("gender")
            age = lst.get("age")
            educations_data = lst.get("education")
            careers_data = lst.get("career")
            awards_data = lst.get("award")
            introduce = lst.get("introduce")
            regions_data = lst.get("region")
            photos = lst.get("image")

            if (
                not author
                or not title
                or not gender
                or not age
                or not introduce
                or not regions_data
            ):
                raise ValidationError("필수 정보가 누락되었습니다.")

            resume.author = author
            resume.title = title
            resume.gender = gender
            resume.age = age
            resume.introduce = introduce
            resume.photos = photos
            resume.save()

            resume.educations.clear()
            for education_data in educations_data:
                education = Education.objects.create(education=education_data)
                resume.educations.add(education)

            resume.careers.clear()
            for career_data in careers_data:
                career = Career.objects.create(career=career_data)
                resume.careers.add(career)

            resume.awards.clear()
            for award_data in awards_data:
                award = Award.objects.create(award=award_data)
                resume.awards.add(award)

            resume.regions.clear()
            for region_data in regions_data:
                region = Region.objects.create(region=region_data)
                resume.regions.add(region)

            serializer = ResumeSerializer(resume)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ResumeDeleteView(BaseUserView):
    def delete(self, request, pk):
        try:
            resume = self.get_object(pk)
            if not resume:
                return JsonResponse(
                    {"error": "Resume not found."}, status=status.HTTP_404_NOT_FOUND
                )

            resume.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response(
                {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
