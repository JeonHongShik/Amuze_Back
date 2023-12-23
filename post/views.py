from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework.response import Response
from .models import Post,wishtype,Image
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
    
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return None

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
        return Post.objects.all()

class PostDetailView(BaseUserView):
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
            data = request.data
            title = data.get("title")
            region = data.get("region")
            concert_type = data.get("concert_type")
            wish_type_ids = data.get("wishtype")
            pay = data.get("pay")
            deadline = data.get("deadline")
            datetime = data.get("datetime")
            introduce = data.get("introduce")
            photos = request.FILES.getlist('photos')

            if not title or not region or not concert_type or not wish_type_ids or not pay or not deadline or not datetime or not introduce:
                return Response(
                    {"detail": "필수 정보가 누락되었습니다."}, status=status.HTTP_400_BAD_REQUEST
                )

            wish_types = []
            for wish_type_id in wish_type_ids:
                try:
                    wish_type = wishtype.objects.get(id=wish_type_id)
                    wish_types.append(wish_type)
                except wishtype.DoesNotExist:
                    return Response({"detail": f"wishtype with id {wish_type_id} does not exist"}, status=status.HTTP_400_BAD_REQUEST)

            post = Post.objects.create(
                author=request.user,
                title=title,
                region=region,
                concert_type=concert_type,
                pay=pay,
                deadline=deadline,
                datetime=datetime,
                introduce=introduce
            )
            post.wish_types.set(wish_types)

            for img in photos:
                Image.objects.create(post=post, image=img)

            serializer = PostSerializer(post)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"detail": "서버 내부 오류가 발생하였습니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PostUpdateView(BaseUserView):
    @transaction.atomic
    def patch(self, request, pk):
        try:
            data = request.data
            post = Post.objects.get(id=pk)
            
            title = data.get("title")
            region = data.get("region")
            concert_type = data.get("concert_type")
            wish_type_ids = data.get("wishtype")
            pay = data.get("pay")
            deadline = data.get("deadline")
            datetime = data.get("datetime")
            introduce = data.get("introduce")
            new_photos = request.FILES.getlist('new_photos')
            delete_photos_ids = data.get("delete_photos_ids", [])

            if not title or not region or not concert_type or not wish_type_ids or not pay or not deadline or not datetime or not introduce:
                return Response(
                    {"detail": "필수 정보가 누락되었습니다."}, status=status.HTTP_400_BAD_REQUEST
                )

            wish_types = []
            for wish_type_id in wish_type_ids:
                try:
                    wish_type = wishtype.objects.get(id=wish_type_id)
                    wish_types.append(wish_type)
                except wishtype.DoesNotExist:
                    return Response({"detail": f"WishType with id {wish_type_id} does not exist"}, status=status.HTTP_400_BAD_REQUEST)

            post.title = title
            post.region = region
            post.concert_type = concert_type
            post.pay = pay
            post.deadline = deadline
            post.datetime = datetime
            post.introduce = introduce
            post.wish_types.set(wish_types)
            post.save()
    
            Image.objects.filter(id__in=delete_photos_ids).delete()
            for img in new_photos:
                Image.objects.create(post=post, image=img)

            serializer = PostSerializer(post)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Post.DoesNotExist:
            return Response({"detail": "Post does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)




class PostDeleteView(BaseUserView):
    @transaction.atomic
    def delete(self, request, pk):
        post = self.get_object(pk)
        if not post:
            return JsonResponse({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            post.delete()
            return JsonResponse({"message": "Post deleted."}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)