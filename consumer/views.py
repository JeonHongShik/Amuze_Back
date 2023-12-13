from rest_framework import generics
from rest_framework.response import Response
from .models import Resume
from .serializers import ResumeSerializer


class ResumeListCreateView(generics.ListCreateAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer


class ResumeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
