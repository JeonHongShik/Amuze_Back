from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import User
from .serializers import UserSerializer
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
import firebase_admin
from firebase_admin import credentials, firestore
from django.http import HttpResponse

class BaseUserView(APIView):
    permission_classes = [AllowAny]

    def get_user(self, uid):
        return get_object_or_404(User, uid=uid)


class accountsViews(APIView):  # 계정 받아오기
    @transaction.atomic
    def post(self, request):
        try:
            cred = credentials.Certificate('amuze.json')
            firebase_admin.initialize_app(cred)

            db = firestore.client()

            users_ref = db.collection(u'User')
            docs = users_ref.stream()

            for doc in docs:
                data = doc.to_dict()
                User.objects.create(uid=data['uid'], name=data['name'], email=data['email'], profile=data['profile'])

            return Response('Sync completed', status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserListView(BaseUserView):  # 유저 정보 보기
    @transaction.atomic
    def get(self, request):
        try:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UpdateUserView(BaseUserView, UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @transaction.atomic
    def patch(self, request, uid, *args, **kwargs):
        try:
            user = self.get_user(uid)

            if request.user.uid != uid:
                return Response(
                    {"detail": "다른 사용자의 정보를 수정할 수 없습니다."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            data = request.data.copy()

            serializer = self.get_serializer(user, data=data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DeleteUserView(BaseUserView):  # 유저 삭제
    @transaction.atomic
    def delete(self, request, uid):
        try:
            user = self.get_user(uid)

            if request.user.uid != uid:
                return Response(
                    {"detail": "다른 사용자의 정보를 삭제할 수 없습니다."},
                    status=status.HTTP_403_FORBIDDEN,
                )
            operation = user.delete()

            if operation:
                response = {"message": "계정 삭제 완료"}

            else:
                response = {"message": "계정 삭제 실패"}

            return Response(response)
        except Exception as e:
            return Response(
                {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# class KakaoLoginCallbackView(BaseUserView):
#     # 카카오 회원 정보를 받아와서 새로운 User 인스턴스를 생성하는 함수
#     @staticmethod
#     def _create_kakao_user(kakao_response):
#         return User.objects.create(
#             uid=kakao_response["id"],
#             name=kakao_response["kakao_account"]["profile"]["nickname"],
#             profile=kakao_response["kakao_account"]["profile"]["profile_image_url"],
#         )

#     # 카카오 액세스 토큰을 통해 사용자 정보를 반환하는 함수
#     @staticmethod
#     def _get_kakao_user_info(access_token):
#         url = "https://kapi.kakao.com/v2/user/me"
#         headers = {
#             "Authorization": f"Bearer {access_token}",
#             "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
#         }
#         response = requests.post(url, headers=headers)
#         response.raise_for_status()
#         return json.loads(response.text)

#     # 카카오 로그인의 콜백을 처리하는 post 메서드
#     def post(self, request):
#         # 요청에서 액세스 토큰을 가져옵니다.
#         kakao_access_code = request.data.get("accessToken")

#         # 액세스 토큰이 제공되지 않았을 경우 에러 메시지와 함께 400 상태 코드를 반환합니다.
#         if not kakao_access_code:
#             return JsonResponse(
#                 {"error": "Kakao access token is required."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#         # 액세스 토큰을 사용하여 카카오 회원 정보를 얻습니다.
#         kakao_response = self._get_kakao_user_info(kakao_access_code)

#         try:
#             # 기존 디비에 있는 사용자 정보를 찾습니다.
#             user_info = User.objects.get(kakaoid=kakao_response["id"])
#             # 기존 사용자는 응답에 ID와 "exist": True를 포함합니다.
#             serializer = UserSerializer(user_info)
#             login(request, user_info)  # 로그인 세션 생성
#             return JsonResponse(serializer.data)
#         except User.DoesNotExist:
#             # 사용자 정보를 찾을 수 없는 경우 새 사용자를 생성합니다.
#             kakao_user = self._create_kakao_user(kakao_response)
#             kakao_user.save()  # 저장
#         return JsonResponse({"id": kakao_user.kakaoid, "exist": False}, status=201)
