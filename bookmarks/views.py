# views.py

from django.http import JsonResponse
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from accounts.models import User
from .models import Postbookmark,Resumebookmark,Boardbookmark
from .serializers import PostFavoriteSerializer,ResumeFavoriteSerializer,BoardFavoriteSerializer
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from django.db import transaction
from django.contrib.auth import get_user_model
from .models import Post,Resume,Board

from post.serializers import PostSerializer
from consumer.serializers import ResumeSerializer
from community.serializers import BoardSerializer

User = get_user_model()

# Post

class GetMyPostBookmarksView(APIView):
    def get(self, request, uid=None):
        if uid is None:
            return JsonResponse({"error": "'uid'가 요청에 포함되지 않았습니다."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = get_user_model().objects.get(uid=uid)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "해당 'uid'를 가진 사용자가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

        posts = Post.objects.filter(author=user)
        if posts.exists():
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data)
        else:
            return JsonResponse({"error": "북마크가 없습니다."}, status=status.HTTP_404_NOT_FOUND)


# class PostBookmarkCreateView(APIView):
#     def post(self, request):
#         uid = request.data.get('uid')
#         if uid is None:
#             return Response({'message': 'uid를 제공해주세요.'}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             author = User.objects.get(uid=uid)
#         except User.DoesNotExist:
#             return Response({'message': '유효하지 않은 uid입니다.'}, status=status.HTTP_404_NOT_FOUND)

#         data = request.data.copy()
#         data['author'] = author.uid
#         serializer = PostFavoriteSerializer(data=data)

#         if serializer.is_valid(raise_exception=True):
#             serializer.save(author=author)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostBookmarkCreateView(APIView):
    def post(self, request):
        uid = request.data.get('uid')
        if uid is None:
            return Response({'message': 'uid를 제공해주세요.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            author = User.objects.get(uid=uid)
        except User.DoesNotExist:
            return Response({'message': '유효하지 않은 uid입니다.'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['author'] = author.uid
        serializer = PostFavoriteSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            post = serializer.save(author=author)
            return Response({'id': post.id, 'post': serializer.data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PostBookmarkDeleteView(APIView):
    @transaction.atomic
    def delete(self, request, pk):
        uid = request.data.get('uid')
        try:
            post = Postbookmark.objects.get(pk=pk, author__uid=uid)
        except Postbookmark.DoesNotExist:
            return JsonResponse({"error": "북마크가 존재하지 않거나 권한이 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            post.delete()
            return JsonResponse({"message": "북마크가 삭제되었습니다."}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"error": f"서버 내부 오류가 발생하였습니다. 오류 내용: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# class CheckPostBookmarkView(APIView):
#     def get(self, request, uid, post_id):
#         try:
#             user = get_user_model().objects.get(uid=uid)
#             post = Post.objects.get(id=post_id)
#         except ObjectDoesNotExist:
#             return JsonResponse({"error": "해당 'uid' 또는 'post_id'를 가진 사용자 또는 게시물이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

#         bookmark = Postbookmark.objects.filter(author=user, post=post).first()
#         if bookmark is not None:
#             return JsonResponse({"bookmark": True}, status=status.HTTP_200_OK)
#         else:
#             return JsonResponse({"bookmark": False}, status=status.HTTP_200_OK)

class CheckPostBookmarkView(APIView):
    def get(self, request, uid, post_id):
        try:
            author = get_user_model().objects.get(uid=uid)
            post = Post.objects.get(id=post_id)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "해당 'uid' 또는 'post_id'를 가진 사용자 또는 게시물이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

        bookmark = Postbookmark.objects.filter(author=author, post=post).first()
        if bookmark is not None:
            return JsonResponse({"bookmark": True, "id": bookmark.id}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"bookmark": False, "id": None}, status=status.HTTP_200_OK)


# Resume
class GetMyResumeBookmarksView(APIView):
    def get(self, request, uid=None):
        if uid is None:
            return JsonResponse({"error": "'uid'가 요청에 포함되지 않았습니다."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = get_user_model().objects.get(uid=uid)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "해당 'uid'를 가진 사용자가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

        resumes = Resume.objects.filter(author=user)
        if resumes.exists():
            serializer = ResumeSerializer(resumes, many=True)
            return Response(serializer.data)
        else:
            return JsonResponse({"error": "북마크가 없습니다."}, status=status.HTTP_404_NOT_FOUND)

class ResumeBookmarkCreateView(APIView):
    def post(self, request):
        uid = request.data.get('uid')
        if uid is None:
            return Response({'message': 'uid를 제공해주세요.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            author = User.objects.get(uid=uid)
        except User.DoesNotExist:
            return Response({'message': '유효하지 않은 uid입니다.'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['author'] = author.uid
        serializer = ResumeFavoriteSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            resume = serializer.save(author=author)
            return Response({'id': resume.id, 'resume': serializer.data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ResumeBookmarkDeleteView(APIView):
    @transaction.atomic
    def delete(self, request, pk):
        uid = request.data.get('uid')
        try:
            resume = Resumebookmark.objects.get(pk=pk, author__uid=uid)
        except Resumebookmark.DoesNotExist:
            return JsonResponse({"error": "이력서 북마크가 존재하지 않거나 권한이 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            resume.delete()
            return JsonResponse({"message": "이력서 북마크가 삭제되었습니다."}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"error": f"서버 내부 오류가 발생하였습니다. 오류 내용: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CheckResumeBookmarkView(APIView):
    def get(self, request, uid, resume_id):
        try:
            user = get_user_model().objects.get(uid=uid)
            resume = Resume.objects.get(id=resume_id)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "해당 'uid' 또는 'resume_id'를 가진 사용자 또는 이력서가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

        bookmark = Resumebookmark.objects.filter(author=user, resume=resume).first()
        if bookmark is not None:
            return JsonResponse({"bookmark": True, "id": bookmark.id}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"bookmark": False,"id": None}, status=status.HTTP_200_OK)
            


        
# Community
class GetMyBoardBookmarksView(APIView):
    def get(self, request, uid):
        if uid is None:
            return JsonResponse({"error": "'uid'가 요청에 포함되지 않았습니다."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = get_user_model().objects.get(uid=uid)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "해당 'uid'를 가진 사용자가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

        boards = Board.objects.filter(author=user)
        if boards.exists():
            serializer = BoardSerializer(boards, many=True)
            return Response(serializer.data)
        else:
            return JsonResponse({"error": "북마크가 없습니다."}, status=status.HTTP_404_NOT_FOUND)

class BoardBookmarkCreateView(APIView):
    def post(self, request):
        uid = request.data.get('uid')
        if uid is None:
            return Response({'message': 'uid를 제공해주세요.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(uid=uid)
        except User.DoesNotExist:
            return Response({'message': '유효하지 않은 uid입니다.'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['user'] = user.uid
        serializer = BoardFavoriteSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            board = serializer.save(author=user)
            return Response({'id': board.id, 'board': serializer.data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class BoardBookmarkDeleteView(APIView):
    @transaction.atomic
    def delete(self, request, pk):
        uid = request.data.get('uid')
        try:
            board = Boardbookmark.objects.get(pk=pk, author__uid=uid)
        except Boardbookmark.DoesNotExist:
            return JsonResponse({"error": "게시판 북마크가 존재하지 않거나 권한이 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            board.delete()
            return JsonResponse({"message": "게시판 북마크가 삭제되었습니다."}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"error": f"서버 내부 오류가 발생하였습니다. 오류 내용: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class CheckBoardBookmarkView(APIView):
    def get(self, request, uid, board_id):
        try:
            user = get_user_model().objects.get(uid=uid)
            board = Board.objects.get(id=board_id)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "해당 'uid' 또는 'board_id'를 가진 사용자 또는 게시글이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

        bookmark = Boardbookmark.objects.filter(author=user, board=board).first()
        if bookmark is not None:
            return JsonResponse({"bookmark": True, "id": bookmark.id}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"bookmark": False,"id": None}, status=status.HTTP_200_OK)