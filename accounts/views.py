import json
from django.shortcuts import get_object_or_404
import requests
from django.http import JsonResponse
from django.contrib.auth import get_user_model, login
from rest_framework.views import APIView
from .serializers import UserSerializer
from .models import User 
from rest_framework.permissions import AllowAny 
from rest_framework.authentication import TokenAuthentication 
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST 
from rest_framework import status

User = get_user_model()

class UserListView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer=UserSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserDetailsView(APIView):
    permission_classes=[AllowAny]
    authentication_classes=[TokenAuthentication]

    def get(self, request, kakaoid):
        user=get_object_or_404(User,kakaoid=kakaoid)
        serializer=UserSerializer(user)
        
        return Response(serializer.data)

class UpdateDeleteUserView(APIView):  
    permission_classes=[AllowAny]  
    authentication_classes=[TokenAuthentication]  

    def put(self,request,kakaoid):  
        user=get_object_or_404(User,kakaoid=kakaoid)  

        data=request.data.copy()  

        if "profile" in request.FILES:  
            user_image=request.FILES["profile"]
            data["profile"]=user_image
        
        serializer=UserSerializer(user,data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) 

        return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)


    def delete(self,request,kakaoid):  
        user=get_object_or_404(User,kakaoid=kakaoid)  
    
        operation=user.delete()  

        if operation:  
            response={"message":"Successfully deleted the requested id"}  

        else:   
            response={"message":"Delete operation failed"}  

        return Response(response)



class KakaoLoginCallbackView(APIView):
    # 카카오 회원 정보를 받아와서 새로운 User 인스턴스를 생성하는 함수
    @staticmethod
    def _create_kakao_user(kakao_response):
        return User.objects.create(
            kakaoid=kakao_response["id"],
            name=kakao_response["kakao_account"]["profile"]["nickname"],
            profile=kakao_response["kakao_account"]["profile"]["profile_image_url"],
        )

    # 카카오 액세스 토큰을 통해 사용자 정보를 반환하는 함수
    @staticmethod
    def _get_kakao_user_info(access_token):
        url = "https://kapi.kakao.com/v2/user/me"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        }
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        return json.loads(response.text)

    # 카카오 로그인의 콜백을 처리하는 post 메서드
    def post(self, request):
    # 요청에서 액세스 토큰을 가져옵니다.
        kakao_access_code = request.data.get("accessToken")

    # 액세스 토큰이 제공되지 않았을 경우 에러 메시지와 함께 400 상태 코드를 반환합니다.
        if not kakao_access_code:
            return JsonResponse(
                {"error": "Kakao access token is required."}, status=HTTP_400_BAD_REQUEST
            )
        # 액세스 토큰을 사용하여 카카오 회원 정보를 얻습니다.
        kakao_response = self._get_kakao_user_info(kakao_access_code)

        try:
            # 기존 디비에 있는 사용자 정보를 찾습니다.
            user_info = User.objects.get(id=kakao_response["id"])
            # 기존 사용자는 응답에 ID와 "exist": True를 포함합니다.
            serializer = UserSerializer(user_info)
            login(request, user_info)  # 로그인 세션 생성
            return JsonResponse(serializer.data)
        except User.DoesNotExist:
    # 사용자 정보를 찾을 수 없는 경우 새 사용자를 생성합니다.
            kakao_user = self._create_kakao_user(kakao_response)
            kakao_user.save()  # 저장
        return JsonResponse({"id": kakao_user.kakaoid, "exist": False}, status=201)