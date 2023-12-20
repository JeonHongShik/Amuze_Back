from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework import generics, permissions, status
from .models import Award, Completion, Education, Career, Region, Resume
from .serializers import ResumeSerializer
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
            return JsonResponse({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ResumeSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)


class ResumeDetailView(BaseUserView):
    def get_object(self,pk):
        try:
            return Resume.objects.get(pk=pk)
        except Resume.DoesNotExist:
            return None

    def get(self, request, pk):
        post_user = self.get_object(pk)
        if not post_user:
            return JsonResponse({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ResumeSerializer(post_user)
        return JsonResponse(serializer.data, safe=False)

class ResumeCreateView(BaseUserView):
    def post(self, request):
        try:
            lst = request.data
            author = lst.get("author")
            phone = lst.get("phone")
            gender = lst.get("gender")
            age = lst.get("age")
            education_data = lst.get("education")
            Career_data = lst.get("Career")
            award_data = lst.get("award")
            completion_data = lst.get("completion")
            introduce = lst.get("introduce")
            Region_data = lst.get("Region")
            image = lst.get("image")

            print(lst)

            # 입력 유효성 검사
            if not author or not phone or not gender or not age or not education_data or not introduce or not Region_data:
                return Response(
                    {"detail": "필수 정보가 누락되었습니다."}, status=status.HTTP_400_BAD_REQUEST
                )

            # 새로운 이력서 객체 생성
            resume = Resume.objects.create(
                author=request.user.uid,
                phone=phone,
                gender=gender,
                age=age,
                education_data=education_data,
                Career_data=Career_data,
                award_data=award_data,
                completion_data=completion_data,
                introduce=introduce,
                Region_data=Region_data,
                image=image
            )

            # ForeignKey 필드에 데이터를 추가
            for education in education_data:
                Education.objects.create(education=education, resume=resume)

            for Career in Career_data:
                Career.objects.create(Career=Career, resume=resume)

            for award in award_data:
                Award.objects.create(award=award, resume=resume)

            for completion in completion_data:
                Completion.objects.create(completion=completion, resume=resume)

            for Region in Region_data:
                Region.objects.create(Region=Region, resume=resume)

            # 생성된 이력서 객체를 직렬화
            serializer = ResumeSerializer(resume)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
