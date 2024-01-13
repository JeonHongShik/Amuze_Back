from django.shortcuts import render
from firebase_admin import messaging
from community.models import Board
from accounts.models import User
from django.http import HttpResponse

def send_to_firebase_cloud_messaging(request, uid):  
    user = User.objects.get(uid=uid)
    registration_token = user.messagingToken
    print('Registration token:', registration_token)

    message = messaging.Message(
    notification=messaging.Notification(
        title='안녕하세요 타이틀 입니다',
        body='안녕하세요 메세지 입니다',
    ),
    token=registration_token,
    )

    response = messaging.send(message)
    print('Successfully sent message:', response)

    return HttpResponse("Message sent successfully")  # 추가된 부분
