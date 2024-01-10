from rest_framework import generics
from rest_framework.response import Response
from .models import Board, Comment
from .serializers import BoardSerializer,CommentSerializer
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db import transaction
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import User

User = get_user_model()

class BaseUserView(APIView):
    def get_user(self, uid):
        return get_object_or_404(User, uid=uid)
    
    def get_object(self, pk):
        try:
            return Board.objects.get(pk=pk)
        except Board.DoesNotExist:
            return None

#Community

class MyCommunityView(BaseUserView):
    def get(self, request, uid):
        communities = Board.objects.filter(author=uid)
        serializer = BoardSerializer(communities, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    
class CommunitylistView(generics.ListAPIView):
    serializer_class = BoardSerializer

    def get_queryset(self):
        return Board.objects.all()

class CommunityDetailView(APIView):
    def get(self, request, pk):
        board = get_object_or_404(Board, pk=pk)

        try:
            serializer = BoardSerializer(board)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"detail": f"서버 내부 오류가 발생하였습니다. 오류 내용: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class CreatecommunityView(BaseUserView):
    @transaction.atomic
    def post(self, request):
        try:
            data = request.data

            board_fields = ["title", "content"]
            board_data = {field: data.get(field) for field in board_fields}

            author = data.get('uid')  # 요청에서 uid를 추출합니다.

            if author is not None:
                try:
                    author = User.objects.get(uid=author)
                except ObjectDoesNotExist:
                    return Response(
                        {"detail": "등록되지 않은 사용자입니다."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {"detail": "'uid' 값이 요청 데이터에 포함되어 있지 않습니다."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            board = Board.objects.create(
                author=author,
                **board_data
            )

            serializer = BoardSerializer(board)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"detail": f"서버 내부 오류가 발생하였습니다. 오류 내용: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )




class UpdatecommunityView(BaseUserView):
    @transaction.atomic
    def patch(self, request, pk):
        uid = request.data.get('uid')  # 요청에서 uid를 추출합니다.
        try:
            # 게시글의 작성자가 요청자와 일치하는지 확인합니다.
            board = Board.objects.get(pk=pk, author__uid=uid)

            data = request.data
            for field in ["title", "content"]:
                if field in data:
                    setattr(board, field, data.get(field))
            
            board.save()

            serializer = BoardSerializer(board)

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Board.DoesNotExist:
            return Response(
                {"detail": "게시글이 존재하지 않거나 권한이 없습니다."},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"detail": f"서버 내부 오류가 발생하였습니다. 오류 내용: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CommunityDeleteView(BaseUserView):
    @transaction.atomic
    def delete(self, request, pk):
        uid = request.data.get('uid')
        
        try:
            community = Board.objects.get(pk=pk, author__uid=uid)
        except Board.DoesNotExist:
            return JsonResponse({"error": "게시글이 존재하지 않거나 권한이 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            community.delete()
            return JsonResponse({"message": "게시글이 삭제되었습니다."}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"error": f"서버 내부 오류가 발생하였습니다. 오류 내용: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





#Comment
class CommentlistView(BaseUserView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.all()


class CommentCreateView(BaseUserView):
    @transaction.atomic
    def post(self, request):
        try:
            data = request.data
            board_id = data.get('board')
            content = data.get('content')

            try:
                board = Board.objects.get(id=board_id)
            except Board.DoesNotExist:
                return Response(
                    {"detail": "해당하는 게시판이 존재하지 않습니다."},
                    status=status.HTTP_404_NOT_FOUND
                )

            uid = data.get('uid')

            if uid is not None:
                try:
                    author = User.objects.get(uid=uid)
                except ObjectDoesNotExist:
                    return Response(
                        {"detail": "등록되지 않은 사용자입니다."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {"detail": "'uid' 값이 요청 데이터에 포함되어 있지 않습니다."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            comment = Comment.objects.create(author=author, board=board, content=content)
            serializer = CommentSerializer(comment)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"detail": f"서버 내부 오류가 발생하였습니다. 오류 내용: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class commentupdateeview(BaseUserView):
    @transaction.atomic
    def patch(self, request, pk):
        uid = request.data.get('uid')
        board_id = request.data.get('board')
        try:
            board = Board.objects.get(pk=board_id)

            comment = Comment.objects.get(pk=pk, author__uid=uid)

            data = request.data
            for field in ["content"]:
                if field in data:
                    setattr(comment, field, data.get(field))
            
            comment.board = board
            comment.save()

            serializer = CommentSerializer(comment)

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Comment.DoesNotExist:
            return Response(
                {"detail": "댓글이 존재하지 않거나 권한이 없습니다."},
                status=status.HTTP_404_NOT_FOUND
            )

        except Board.DoesNotExist:
            return Response(
                {"detail": "해당하는 게시글이 존재하지 않습니다."},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"detail": f"서버 내부 오류가 발생하였습니다. 오류 내용: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    
class commentdeleteview(BaseUserView):
    def delete(self, request, pk):
        uid = request.data.get('uid')
        try:
            comment = Comment.objects.get(pk=pk, author__uid=uid)
        except Comment.DoesNotExist:
            return Response({"detail": "댓글이 존재하지 않거나 권한이 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            comment.delete()
            return Response({"message": "댓글이 삭제되었습니다."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": f"서버 내부 오류가 발생하였습니다. 오류 내용: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#add count
class AddLikeView(APIView):
    def post(self, request, pk):
        board = get_object_or_404(Board, pk=pk)
        uid = request.data.get('uid')
        user = get_object_or_404(User, uid=uid)

        if user in board.likes.all():
            board.likes.remove(user)
            message = "좋아요가 취소되었습니다."
            check_like = False
        else:
            board.likes.add(user)
            message = "좋아요가 추가되었습니다."
            check_like = True

        board.save()  

        return Response({"like_count": board.like_count, "message": message, "check_like": check_like})

