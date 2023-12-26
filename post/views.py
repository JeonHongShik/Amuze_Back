from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer
from django.http import JsonResponse
from django.db import transaction
from rest_framework import generics,status


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
            mainimage = request.FILES.get('mainimage')
            otherimages1 = request.FILES.get('otherimages1')
            otherimages2 = request.FILES.get('otherimages2')
            otherimages3 = request.FILES.get('otherimages3')
            otherimages4 = request.FILES.get('otherimages4')

            post_fields = ["title", "region", "type", "pay", "deadline", "datetime", "introduce", "wishtype"]
            post_data = {field: data.get(field) for field in post_fields}


            #나중에 지워야함!
            if request.user.is_authenticated:
                author = request.user
            else:
                author = None 
                #나중에 지워야함!



            post = Post.objects.create(
                author=author,
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



class PostUpdateView(BaseUserView):
    @transaction.atomic
    def patch(self, request, pk):
        try:
            data = request.data
            post = Post.objects.get(id=pk)

            post_fields = ["title", "region", "type", "wishtype", "pay", "deadline", "datetime", "introduce"]

            for field in post_fields:
                if field in data:
                    setattr(post, field, data[field])

            image_fields = ["mainimage", "otherimages1", "otherimages2", "otherimages3", "otherimages4"]
            for image_field in image_fields:
                image_file = request.FILES.get(image_field)
                if image_file:
                    setattr(post, image_field, image_file)

            post.save()

            serializer = PostSerializer(post)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Post.DoesNotExist:
            return Response({"detail": "게시물이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": f"서버 내부 오류가 발생하였습니다. 오류 내용: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)






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