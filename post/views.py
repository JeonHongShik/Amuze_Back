from django.shortcuts import get_object_or_404
from requests import request
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer
from django.http import JsonResponse
from django.db import transaction
from rest_framework import generics,status
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

#API 테스트용
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

#유저찾기
User = get_user_model()

class BaseUserView(APIView):
    def get_user(self, uid):
        return get_object_or_404(User, uid=uid)
    
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return None

class GetMyPostView(BaseUserView):
    def get(self, request, uid):
        posts = Post.objects.filter(author=uid)
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
            mainimage = request.FILES.get('mainimage')
            otherimages1 = request.FILES.get('otherimages1')
            otherimages2 = request.FILES.get('otherimages2')
            otherimages3 = request.FILES.get('otherimages3')
            otherimages4 = request.FILES.get('otherimages4')

            post_fields = ["title", "region", "type", "pay", "deadline", "datetime", "introduce", "wishtype"]
            post_data = {field: data.get(field) for field in post_fields}

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

            post = Post.objects.create(
                author=user,
                mainimage=mainimage,
                otherimages1=otherimages1,
                otherimages2=otherimages2,
                otherimages3=otherimages3,
                otherimages4=otherimages4,
                **post_data
            )

            serializer = PostSerializer(post)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"detail": f"서버 내부 오류가 발생하였습니다. 오류 내용: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    
# class PostUpdateView(BaseUserView):
#     @transaction.atomic
#     def patch(self, request, pk):
#         uid = request.data.get('uid')
#         try:
#             post = Post.objects.get(id=pk, author__uid=uid)

#             data = request.data
#             post_fields = ["title", "region", "type", "wishtype", "pay", "deadline", "datetime", "introduce"]
#             post_data = {field: data.get(field) for field in post_fields}

#             for field, value in post_data.items():
#                 setattr(post, field, value)

#             post.mainimage = request.FILES.get("mainimage", post.mainimage)
#             post.otherimages1 = request.FILES.get("otherimages1", post.otherimages1)
#             post.otherimages2 = request.FILES.get("otherimages2", post.otherimages2)
#             post.otherimages3 = request.FILES.get("otherimages3", post.otherimages3)
#             post.otherimages4 = request.FILES.get("otherimages4", post.otherimages4)

#             post.save()

#             serializer = PostSerializer(post)

#             return Response(serializer.data, status=status.HTTP_200_OK)

#         except Post.DoesNotExist:
#             return Response({"detail": "게시물이 존재하지 않거나 권한이 없습니다."}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({"detail": f"서버 내부 오류가 발생하였습니다. 오류 내용: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PostUpdateView(BaseUserView):
    @transaction.atomic
    def patch(self, request, pk):
        uid = request.data.get('uid')
        try:
            post = Post.objects.get(id=pk, author__uid=uid)

            data = request.data
            post_fields = ["title", "region", "type", "wishtype", "pay", "deadline", "datetime", "introduce"]
            post_data = {field: data.get(field) for field in post_fields}

            for field, value in post_data.items():
                setattr(post, field, value)

            image_fields = ["mainimage", "otherimages1", "otherimages2", "otherimages3", "otherimages4"]
            for img_field in image_fields:
                if img_field in request.FILES:
                    setattr(post, img_field, request.FILES.get(img_field))
                elif data.get(img_field) in [None, 'null']:
                    setattr(post, img_field, None)

            post.save()

            serializer = PostSerializer(post)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Post.DoesNotExist:
            return Response({"detail": "게시물이 존재하지 않거나 권한이 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": f"서버 내부 오류가 발생하였습니다. 오류 내용: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class PostDeleteView(BaseUserView):
    @transaction.atomic
    def delete(self, request, pk):
        uid = request.data.get('uid')
        try:
            post = Post.objects.get(id=pk, author__uid=uid)
            post.delete()
            return JsonResponse({"message": "Post deleted."}, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return JsonResponse({"error": "게시물이 존재하지 않거나 권한이 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)