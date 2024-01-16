from django.shortcuts import render
from firebase_admin import messaging
from community.models import Board,Comment
from accounts.models import User
from django.http import HttpResponse
from django.db.models.signals import post_save
from django.dispatch import receiver

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


@receiver(post_save, sender=Comment)
def send_to_firebase_cloud_messaging(sender, instance, created, **kwargs):
    if created:
        user = instance.author
        registration_token = user.messagingToken
        print('Registration token:', registration_token)
        
        
        message = messaging.Message(
            notification=messaging.Notification(
                title='커뮤니티 새로운 댓글 알림',
                body=f'사용자님의 게시글에 새로운 댓글이 달렸습니다.
                        {instance.content}',
            ),
            data={'baord_id':str(instance.board.id),
            },
            token=registration_token,
        )
        
        
        response = messaging.send(message)
        print('Successfully sent message:', response)