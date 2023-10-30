from django.db import transaction
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from .serializers import ConsumerSerializer
from rest_framework.response import Response
from .models import consumer

# Create your views here.

class BaseUserView(APIView):
    permisson_classes = [AllowAny]

    def get_user(self, kakaoid):
        return get_object_or_404(User, kakaoid=kakaoid)

class WriteConsumerView(BaseUserView):

    @transaction.atomic
    def post(self, request):
        lst = request.data
        title = lst.get('title')
        author = lst.get('author')
        profile = lst.get('profile')
        age = lst.get('age')
        education = lst.get('education')
        career = lst.get('career')

        print(lst)
        serializer = ConsumerSerializer(data=lst)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "201", "data": serializer.data}, status=status.HTTP_201_CREATED)

        return Response({"status": "400", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class ConsumerListView(BaseUserView):

    def get(self, request):
        Consumers = consumer.objects.all()
        serializer = ConsumerSerializer(Consumers, many=True)
        return Response({"message": "200 오류아님", "data": serializer.data}, status=status.HTTP_200_OK)


