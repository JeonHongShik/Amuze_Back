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
                {"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND
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
                {"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = ResumeSerializer(post_user)
        return JsonResponse(serializer.data, safe=False)


class ResumeCreateView(BaseUserView):
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

            # 입력 유효성 검사
            if (
                not author
                or not title
                or not gender
                or not age
                or not introduce
                or not regions_data
            ):
                raise ValidationError("필수 정보가 누락되었습니다.")

            # 새로운 이력서 객체 생성
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
                photos=photos,
            )

            # ForeignKey 필드에 데이터를 추가
            for educations in educations_data:
                Education.objects.create(education=Education, resume=resume)

            for careers in careers_data:
                Career.objects.create(Career=Career, resume=resume)

            for awards in awards_data:
                Award.objects.create(award=Award, resume=resume)

            for regions in regions_data:
                Region.objects.create(Region=Region, resume=resume)

            # 생성된 이력서 객체를 직렬화
            serializer = ResumeSerializer(resume)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
