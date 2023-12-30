from django.db.models import Q
from rest_framework import generics
from consumer.serializers import ResumeSerializer
from post.serializers import PostSerializer
from community.serializers import BoardSerializer
from consumer.models import Resume
from post.models import Post
from community.models import Board
from rest_framework.pagination import PageNumberPagination
from django.views.decorators.cache import cache_page # 캐싱처리

class Paging(PageNumberPagination):
    page_size = 10

class BaseSearchView(generics.ListAPIView):
    pagination_class = Paging

    def get_queryset(self):
        raise NotImplementedError()

    def get_query(self):
        query = self.request.GET.get('q')
        if not query:
            return None
        return query.strip()


class PostSearchView(BaseSearchView):
    serializer_class = PostSerializer

    @cache_page(60 * 10) 
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        query = self.get_query()
        if not query:
            return Post.objects.none()
        return Post.objects.filter(
            Q(title__contains=query) | 
            Q(region__contains=query) | 
            Q(type__contains=query) | 
            Q(pay__contains=query) | 
            Q(wishtype__contains=query) | 
            Q(deadline__contains=query) | 
            Q(datetime__contains=query) | 
            Q(introduce__contains=query) | 
            Q(author__displayName__contains=query)
        )

class BoardSearchView(BaseSearchView):
    serializer_class = BoardSerializer

    @cache_page(60 * 10) 
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        query = self.get_query()
        if not query:
            return Board.objects.none()
        return Board.objects.filter(
            Q(title__contains=query) | 
            Q(content__contains=query)
        )
    
class ResumeSearchView(BaseSearchView):
    serializer_class = ResumeSerializer

    @cache_page(60 * 15)  # 15분 동안 캐시
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        query = self.get_query()
        if not query:
            return Resume.objects.none()
        return Resume.objects.filter(
            Q(title__contains=query) | 
            Q(gender__contains=query) | 
            Q(age__contains=query) | 
            Q(introduce__contains=query) |
            Q(educations__education__contains=query) |
            Q(careers__career__contains=query) |
            Q(awards__award__contains=query) |
            Q(regions__region__contains=query) |
            Q(author__displayName__contains=query)
        )