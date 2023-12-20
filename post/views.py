from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework.response import Response
from .models import Post,WishType,Image
from .serializers import PostSerializer
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from django.http import JsonResponse
from django.db import transaction
from rest_framework import generics, permissions, status
from django.core.files.base import ContentFile
import base64
from django.db import transaction


#API 테스트용
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator



class BaseUserView(APIView):
    permission_classes = [AllowAny]
    # permission_classes = [permissions.IsAuthenticated]
    def get_user(self, uid):
        return get_object_or_404(User, uid=uid)



class GetMyPostView(BaseUserView):
    def get(self, request):
        try:
            posts = Post.objects.filter(author=request.user.uid)
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        try:
            return Post.objects.all()
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PostDetailView(BaseUserView):
    def get_object(self,pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return None
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, pk):
        post_user = self.get_object(pk)
        if not post_user:
            return JsonResponse({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
        try:
            serializer = PostSerializer(post_user)
            return JsonResponse(serializer.data, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PostCreateView(BaseUserView):
    @transaction.atomic
    def post(self, request):
        try:
            lst = request.data
            author = lst.get("author")
            title = lst.get("title")
            area = lst.get("area")
            concert_type = lst.get("concert_type")
            wish_type_ids = lst.get("wish_type")
            pay = lst.get("pay")
            deadline = lst.get("deadline")
            playtime = lst.get("playtime")
            content = lst.get("content")
            images = request.FILES.getlist('images')

            # 입력 유효성 검사
            if not title or not author or not area or not concert_type or not wish_type_ids or not pay or not deadline or not playtime or not content or not images:
                return Response(
                    {"detail": "필수 정보가 누락되었습니다."}, status=status.HTTP_400_BAD_REQUEST
                )

            # 새로운 게시글 객체 생성
            post = Post.objects.create(
                author=request.user,
                title=title,
                area=area,
                concert_type=concert_type,
                pay=pay,
                deadline=deadline,
                playtime=playtime,
                content=content,
            )

            for img in images:
                image = Image.objects.create(post=post, images=img)

            for wish_type_id in wish_type_ids:
                wish_type = WishType.objects.get(id=wish_type_id)
                post.wish_types.add(wish_type)

            # 생성된 게시글 객체를 직렬화
            serializer = PostSerializer(post)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class PostUpdateView(BaseUserView, UpdateAPIView):
    serializer_class = PostSerializer

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return None
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @transaction.atomic
    def put(self, request, pk):
        post = self.get_object(pk)
        if not post:
            return JsonResponse({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            serializer = PostSerializer(post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class PostDeleteView(BaseUserView):
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return None
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @transaction.atomic
    def delete(self, request, pk):
        post = self.get_object(pk)
        if not post:
            return JsonResponse({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            post.delete()
            return JsonResponse({"message": "Post deleted."}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)