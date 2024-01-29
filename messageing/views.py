from gettext import translation
from django.shortcuts import render
from firebase_admin import messaging
from community.models import Board,Comment
from accounts.models import User
from django.http import HttpResponse
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.response import Response
from messageing.serializers import NotificationSerializer
from .models import Notification 
from rest_framework.views import APIView
from rest_framework import status
from django.db import transaction


@receiver(post_save, sender=Comment)
def send_to_firebase_cloud_messaging(sender, instance, created, **kwargs):
    if created:
        # 게시글 작성자를 가져옵니다.
        user = instance.board.author
        # 댓글 작성자를 가져옵니다.
        comment_author = instance.author
        
        # 게시글 작성자와 댓글 작성자가 동일한 경우, 알림을 보내지 않습니다.
        if user == comment_author:
            return

        registration_token = user.messagingToken
        print('Registration token:', registration_token)

        message = messaging.Message(
            notification=messaging.Notification(
                title='새로운 댓글 알림',
                body=f'{instance.board.title}새로운 댓글이 달렸어요!',
            ),
            data={'board_id':str(instance.board.id)},
            token=registration_token,
        )

        response = messaging.send(message)
        print('Successfully sent message:', response)

        Notification.objects.create(
            uid=user,
            title=instance.board,
            messagebody=message.notification.body,
            content=f'{instance.content}',
            board_id=instance.board.id,
        )

# @receiver(post_save, sender=Comment)
# def send_to_firebase_cloud_messaging(sender, instance, created, **kwargs):
#     if created:
#         user = instance.board.author
#         registration_token = user.messagingToken
#         print('Registration token:', registration_token)

#         message = messaging.Message(
#             notification=messaging.Notification(
#                 title='새로운 댓글 알림',
#                 body=f'{instance.board.title}\n 새로운 댓글이 달렸어요!',
#             ),
#             data={'board_id':str(instance.board.id)},
#             token=registration_token,
#         )

#         response = messaging.send(message)
#         print('Successfully sent message:', response)

#         Notification.objects.create(
#             uid=user,
#             title=instance.board.title,
#             content=f'{instance.board.title} 새로운 댓글이 달렸어요!',
#             board_id=instance.board,  # 수정된 부분
#         )

        
class mynotificationsviews(APIView):
    def get(self, request, uid, format=None):
        notifications = Notification.objects.filter(uid=uid)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)
    
class NotificationDeleteView(APIView):
    def delete(self, request, pk):
        uid = request.data.get('uid')
        try:
            notification = Notification.objects.get(pk=pk, uid=uid)
        except Notification.DoesNotExist:
            return Response({"detail": "알림이 존재하지 않거나 권한이 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            notification.delete()
            return Response({"message": "알림이 삭제되었습니다."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": f"서버 내부 오류가 발생하였습니다. 오류 내용: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    
# def send_to_firebase_cloud_messaging(request, uid):  
#     user = User.objects.get(uid=uid)
#     registration_token = user.messagingToken
#     print('Registration token:', registration_token)

#     message = messaging.Message(
#     notification=messaging.Notification(
#         title='안녕하세요 타이틀 입니다',
#         body='안녕하세요 메세지 입니다',
#     ),
#     token=registration_token,
#     )

#     response = messaging.send(message)
#     print('Successfully sent message:', response)

#     return HttpResponse("Message sent successfully")


# @receiver(post_save, sender=Comment)
# def send_to_firebase_cloud_messaging(sender, instance, created, **kwargs):
#     if created:
#         user = instance.author
#         registration_token = user.messagingToken
#         print('Registration token:', registration_token)
        
        
#         message = messaging.Message(
#             notification=messaging.Notification(
#                 title='새로운 댓글 알림',
#                 body=f'{instance.board.title}\n 새로운 댓글이 달렸어요!',
#             ),
#             data={'board_id':str(instance.board.id),
#             },
#             token=registration_token,
#         )
        
        
#         response = messaging.send(message)
#         print('Successfully sent message:', response)