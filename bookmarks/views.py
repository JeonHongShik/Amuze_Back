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

User = get_user_model()

# Post

class GetMyPostBookmarksView(APIView):
    def get(self, request, uid=None):
        if uid is None:
            return JsonResponse({"error": "'uid'가 요청에 포함되지 않았습니다."}, status=status.HTTP_400_BAD_REQUEST)

        posts = Postbookmark.objects.filter(author__uid=uid)
        if posts.exists():
            serializer = PostFavoriteSerializer(posts, many=True)
            return Response(serializer.data)
        else:
            return JsonResponse({"error": "북마크가 없습니다."}, status=status.HTTP_404_NOT_FOUND)


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
            serializer.save(author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

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




# Resume
class GetMyResumeBookmarksView(APIView):
    def get(self, request, uid=None):
        if uid is None:
            return JsonResponse({"error": "'uid'가 요청에 포함되지 않았습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = get_user_model().objects.get(uid=uid)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "해당 'uid'를 가진 사용자가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

        resumes = Resumebookmark.objects.filter(author=user)
        if resumes.exists():
            serializer = ResumeFavoriteSerializer(resumes, many=True)
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
            serializer.save(author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

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




        
# Community
class GetMyBoardBookmarksView(APIView):
    def get(self, request, uid):
        if uid is None:
            return JsonResponse({"error": "'uid'가 요청에 포함되지 않았습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = get_user_model().objects.get(uid=uid)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "해당 'uid'를 가진 사용자가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

        boards = Boardbookmark.objects.filter(author=user)
        if boards.exists():
            serializer = BoardFavoriteSerializer(boards, many=True)
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
            serializer.save(author=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

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
