from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import generics, status
from .models import Award, Education, Career, Region, Resume
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
            data = request.data
            mainimage = request.FILES.get('mainimage')
            otherimages1 = request.FILES.get('otherimages')
            otherimages2 = request.FILES.get('otherimages2')
            otherimages3 = request.FILES.get('otherimages3')
            otherimages4 = request.FILES.get('otherimages4')

            resume_fields = ["title", "gender", "age", "introduce"]
            resume_data = {field: data.get(field) for field in resume_fields}

            if request.user.is_authenticated:
                author = request.user
            else:
                author = None 

            resume = Resume.objects.create(
                author=author,
                mainimage=mainimage,
                otherimages1=otherimages1,
                otherimages2=otherimages2,
                otherimages3=otherimages3,
                otherimages4=otherimages4,
                **resume_data
            )

            educations_data = data.get("education").split(',')
            careers_data = data.get("career").split(',')
            awards_data = data.get("award").split(',')
            regions_data = data.get("region").split(',')

            Education.objects.bulk_create(
                [Education(education=education.strip(), resume=resume) for education in educations_data]
            )

            Career.objects.bulk_create(
                [Career(career=career.strip(), resume=resume) for career in careers_data]
            )

            Award.objects.bulk_create(
                [Award(award=award.strip(), resume=resume) for award in awards_data]
            )

            Region.objects.bulk_create(
                [Region(region=region.strip(), resume=resume) for region in regions_data]
            )

            serializer = ResumeSerializer(resume)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"detail": f"서버 내부 오류가 발생하였습니다. 오류 내용: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )





class ResumeUpdateView(BaseUserView):
    @transaction.atomic
    def patch(self, request, pk):
        try:
            data = request.data
            resume = Resume.objects.get(id=pk)

            resume_fields = ["author", "title", "gender", "age", "introduce"]
            resume_data = {field: data.get(field) for field in resume_fields}

            for field, value in resume_data.items():
                setattr(resume, field, value)

            resume.mainimage = request.FILES.get("mainimage", resume.mainimage)
            resume.otherimages1 = request.FILES.get("otherimages1", resume.otherimages1)
            resume.otherimages2 = request.FILES.get("otherimages2", resume.otherimages2)
            resume.otherimages3 = request.FILES.get("otherimages3", resume.otherimages3)
            resume.otherimages4 = request.FILES.get("otherimages4", resume.otherimages4)

            resume.save()

            related_fields = ["educations", "careers", "awards", "regions"]
            for related_field in related_fields:
                if related_field in data:
                    getattr(resume, related_field).clear()
                    for related_data in data.get(related_field):
                        related_object = globals()[related_field.capitalize()].objects.create(data=related_data)
                        getattr(resume, related_field).add(related_object)

            serializer = ResumeSerializer(resume)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Resume.DoesNotExist:
            return Response({"detail": "이력서가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": f"서버 내부 오류가 발생하였습니다. 오류 내용: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
