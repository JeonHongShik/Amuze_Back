from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import User
from .serializers import UserSerializer
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, DestroyAPIView
import firebase_admin
from firebase_admin import credentials, firestore ,auth
from django.http import Http404, HttpResponse
from firebase_admin import db
from django.contrib.auth import get_user_model

cred = credentials.Certificate('amuze.json')
firebase_admin.initialize_app(cred)

User = get_user_model()

class BaseUserView(APIView):

    def get_user(self, uid):
        return get_object_or_404(User, uid=uid)
    
class SignupFirebaseView(BaseUserView):
    def get(self, request):
        db = firestore.client()

        firebase_users = db.collection('users').get()
        firebase_user_ids = [user.id for user in firebase_users]

        django_users = User.objects.all()

        for user in django_users:
            if user.uid not in firebase_user_ids and not (user.is_staff or user.is_superuser):
                user.delete()

        for user in firebase_users:
            if not User.objects.filter(uid=user.id).exists():
                # 사용자가 Django에서 존재하지 않으면, 생성
                User.objects.create(
                    uid=user.id,
                    displayName=user.to_dict().get('displayName'),
                    email=user.to_dict().get('email'),
                    photoURL=user.to_dict().get('photoURL', "")
                )
            else:
                # 사용자가 Django에서 존재하면, 업데이트
                django_user = User.objects.get(uid=user.id)
                django_user.displayName = user.to_dict().get('displayName')
                django_user.email = user.to_dict().get('email')
                django_user.photoURL = user.to_dict().get('photoURL', "")
                django_user.save()

        return Response('회원가입 완료', status=status.HTTP_201_CREATED)





class syncdbfirebase(APIView):
    def post(self, request):
        try:
            cred = credentials.Certificate('amuze.json')
            firebase_admin.initialize_app(cred)

            db = firestore.client()

            users_ref = db.collection(u'User')
            docs = users_ref.stream()

            for doc in docs:
                data = doc.to_dict()
                user = User.objects.create(uid=data['uid'], name=data['name'], email=data['email'], profile=data['profile'])
                user.save()
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

    def get(self, request, uid, *args, **kwargs):
        try:
            user = self.queryset.get(uid=uid)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            raise Http404


class UpdateUserView(BaseUserView, UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'uid'
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


# class localsignupview(BaseUserView):
#     @transaction.atomic
#     def post(self, request):
#         try:
#             lst = request.data
#             uid = lst.get("uid")
#             name = lst.get("name")
#             profile = lst.get("profile")
#             email = lst.get("email")

#             print(lst)

#             # 입력 유효성 검사
#             if not uid or not name or not email:
#                 return Response(
#                     {"detail": "필수 정보가 누락되었습니다."}, status=status.HTTP_400_BAD_REQUEST
#                 )

#             # 이미 존재하는 사용자 체크 및 생성
#             user, created = User.objects.get_or_create(
#                 uid=uid,
#                 defaults={
#                     "name": name,
#                     "profile": profile,
#                     "email": email,
#                 },
#             )

#             if not created:
#                 return Response(
#                     {"detail": "이미 가입된 사용자입니다."}, status=status.HTTP_400_BAD_REQUEST
#                 )

#             serializer = UserSerializer(user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

#         except Exception as e:
#             return Response(
#                 {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )