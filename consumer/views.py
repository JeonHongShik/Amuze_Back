from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import generics, status
from .models import Award, Education, Career, Region, Resume
from .serializers import ResumeSerializer
from rest_framework.exceptions import ValidationError
from django.db import transaction
import json
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()

class BaseUserView(APIView):
    def get_user(self, uid):
        return get_object_or_404(User, uid=uid)


class ResumeListView(generics.ListAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer


class GetMyResumeView(BaseUserView):
    def get(self, request, uid):
        resumes = Resume.objects.filter(author=uid)
        serializer = ResumeSerializer(resumes, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)


class ResumeDetailView(BaseUserView):
    def get_object(self, pk):
        try:
            return Resume.objects.get(pk=pk)
        except Resume.DoesNotExist:
            return None

    def get(self, request, pk):
        resume_user = self.get_object(pk)
        if not resume_user:
            return JsonResponse(
                {"error": "정보를 찾을 수 없습니다"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = ResumeSerializer(resume_user)
        return JsonResponse(serializer.data, safe=False)
        
        
class ResumeCreateView(BaseUserView):
    @transaction.atomic
    def post(self, request):
        try:
            data = request.data
            mainimage = request.FILES.get('mainimage')
            otherimages1 = request.FILES.get('otherimages1')
            otherimages2 = request.FILES.get('otherimages2')
            otherimages3 = request.FILES.get('otherimages3')
            otherimages4 = request.FILES.get('otherimages4')

            resume_fields = ["title", "gender", "age", "introduce"]
            resume_data = {field: data.get(field) for field in resume_fields}

            uid = data.get('uid')
            if uid is not None:
                try:
                    user = User.objects.get(uid=uid)
                except ObjectDoesNotExist:
                    return Response(
                        {"detail": "해당 uid를 가진 사용자가 존재하지 않습니다."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {"detail": "'uid' 값이 요청 데이터에 포함되어 있지 않습니다."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            resume = Resume.objects.create(
                author=user,
                mainimage=mainimage,
                otherimages1=otherimages1,
                otherimages2=otherimages2,
                otherimages3=otherimages3,
                otherimages4=otherimages4,
                **resume_data
            )
            educations_data = data.get("education").split(',')
            careers_data = [data.get("career")] if ',' not in data.get("career") else data.get("career").split(',')
            awards_data = [data.get("award")] if ',' not in data.get("award") else data.get("award").split(',')
            regions_data = [data.get("region")] if ',' not in data.get("region") else data.get("region").split(',')


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
        uid = request.data.get('uid') 
        try:

            resume = Resume.objects.get(id=pk, author__uid=uid)

            data = request.data
            resume_fields = ["title", "gender", "age", "introduce"]
            resume_data = {field: data.get(field) for field in resume_fields}

            for field, value in resume_data.items():
                setattr(resume, field, value)

            resume.mainimage = request.FILES.get("mainimage", resume.mainimage)
            resume.otherimages1 = request.FILES.get("otherimages1", resume.otherimages1)
            resume.otherimages2 = request.FILES.get("otherimages2", resume.otherimages2)
            resume.otherimages3 = request.FILES.get("otherimages3", resume.otherimages3)
            resume.otherimages4 = request.FILES.get("otherimages4", resume.otherimages4)

            resume.save()

            related_models = {
                "educations": Education,
                "careers": Career,
                "awards": Award,
                "regions": Region
            }

            for related_field, RelatedModel in related_models.items():
                if related_field in data:
                    # 기존 연결된 객체 삭제
                    getattr(resume, related_field).all().delete()
                    # 새로운 객체 생성 및 연결
                    items_data = data.get(related_field).split(',')
                    RelatedModel.objects.bulk_create(
                        [RelatedModel(resume=resume, **{related_field[:-1]: item.strip()}) for item in items_data]
                    )

            serializer = ResumeSerializer(resume)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Resume.DoesNotExist:
            return Response({"detail": "이력서가 존재하지 않거나 권한이 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": f"서버 내부 오류가 발생하였습니다. 오류 내용: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class ResumeDeleteView(BaseUserView):
    @transaction.atomic
    def delete(self, request, pk):
        uid = request.data.get('uid')
        try:
            resume = Resume.objects.get(id=pk, author__uid=uid)

            resume.delete()
            return JsonResponse({"message": "이력서가 삭제되었습니다."}, status=status.HTTP_200_OK)

        except Resume.DoesNotExist:
            return JsonResponse({"error": "이력서가 존재하지 않거나 권한이 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
