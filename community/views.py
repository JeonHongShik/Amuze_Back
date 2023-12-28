from rest_framework import generics
from rest_framework.response import Response
from .models import Board, Comment
from .serializers import BoardSerializer,CommentSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db import transaction
from django.http import JsonResponse

class BaseUserView(APIView):
    permission_classes = [AllowAny]
    # permission_classes = [permissions.IsAuthenticated]
    def get_user(self, uid):
        return get_object_or_404(User, uid=uid)
    
    def get_object(self, pk):
        try:
            return Board.objects.get(pk=pk)
        except Board.DoesNotExist:
            return None

#Community
        

class MyCommunityView(APIView):
    def get(self, request):
        try:
            communities = Board.objects.filter(author=request.user.uid)
        except Board.DoesNotExist:
            return Response({"detail": "커뮤니티를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        serializer = BoardSerializer(communities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CommunitylistView(generics.ListAPIView):
    serializer_class = BoardSerializer

    def get_queryset(self):
        return Board.objects.all()

class CommunityDetailView(APIView):
    def get(self, request, pk):
        board = get_object_or_404(board, pk=pk)

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

            if request.user.is_authenticated:
                writer = request.user
            else:
                writer = None

            board = Board.objects.create(
                writer=writer,
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
        try:
            board = Board.objects.get(pk=pk)
            data = request.data

            for field in ["title", "content"]:
                if field in data:
                    setattr(board, field, data.get(field))
            
            board.save()

            serializer = BoardSerializer(board)

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Board.DoesNotExist:
            return Response(
                {"detail": "해당 게시글이 존재하지 않습니다."},
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
        community = self.get_object(pk)
        if not community:
            return JsonResponse({"error": "community not found."}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            community.delete()
            return JsonResponse({"message": "community deleted."}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

            # 'board' 필드에 대해 Board 인스턴스를 할당
            try:
                board = Board.objects.get(id=board_id)
            except Board.DoesNotExist:
                return Response(
                    {"detail": "해당하는 게시판이 존재하지 않습니다."},
                    status=status.HTTP_404_NOT_FOUND
                )

            if request.user.is_authenticated:
                writer = request.user
            else:
                writer = None

            comment = Comment.objects.create(writer=writer, board=board, content=content)
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
        try:
            comment = Comment.objects.get(pk=pk)
            data = request.data

            for field in ["board", "content"]:
                if field in data:
                    setattr(comment, field, data.get(field))
            
            comment.save()

            serializer = CommentSerializer(comment)

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Comment.DoesNotExist:
            return Response(
                {"detail": "해당 댓글이 존재하지 않습니다."},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"detail": f"서버 내부 오류가 발생하였습니다. 오류 내용: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
class commentdeleteview(BaseUserView):
    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        if not comment:
            return Response({"error": "comment not found."}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            comment.delete()
            return Response({"message": "comment deleted."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#add count
class AddLikeView(APIView):
    def post(self, request, pk):
        board = get_object_or_404(Board, pk=pk)
        user = request.user
        board.likes.add(user)
        board.save()

        return Response({"like_count": board.like_count})