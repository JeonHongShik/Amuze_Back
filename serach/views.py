from django.db.models import Q
from rest_framework import generics
from consumer.serializers import ResumeSerializer
from post.serializers import PostSerializer
from community.serializers import BoardSerializer
from consumer.models import Resume
from post.models import Post
from community.models import Board
from rest_framework.pagination import PageNumberPagination


class BaseSearchView(generics.ListAPIView):
    def get_queryset(self):
        raise NotImplementedError()

    def get_query(self):
        query = self.request.GET.get('q')
        if not query:
            return None
        return query.strip()


class PostSearchView(BaseSearchView):
    serializer_class = PostSerializer

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
        ).distinct()

class BoardSearchView(BaseSearchView):
    serializer_class = BoardSerializer

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        query = self.get_query()
        if not query:
            return Board.objects.none()
        return Board.objects.filter(
            Q(title__contains=query) | 
            Q(content__contains=query)
        ).distinct()
    
class ResumeSearchView(BaseSearchView):
    serializer_class = ResumeSerializer

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
        ).distinct()
        
        


class ResumeKeywordSearchView(BaseSearchView):
    serializer_class = ResumeSerializer

    def get_queryset(self):
        region_values = self.request.GET.getlist('region', [])
        gender_values = self.request.GET.getlist('gender', [])
        education_values = self.request.GET.getlist('education', [])

        # Initialize queryset
        queryset = Resume.objects.all()

        # Apply region filter
        for region_value in region_values:
            queryset = queryset.filter(regions__region__icontains=region_value.strip())

        # Apply gender filter
        for gender_value in gender_values:
            queryset = queryset.filter(gender__icontains=gender_value.strip())

        # Apply education filter
        for education_value in education_values:
            queryset = queryset.filter(educations__education__icontains=education_value.strip())

        return queryset.distinct()





# class ResumeKeywordSearchView(BaseSearchView):
#     serializer_class = ResumeSerializer

#     def get_queryset(self):
#         region_values=self.request.GET.getlist('region',[])
        
#         if len(region_values) > 1:
#             queryset = Resume.objects.filter(regions__region__icontains=region_values[0].strip())
        
#             for region_value in region_values[1:]:
#                 queryset = queryset.filter(regions__region__icontains=region_value.strip())
                
#         else:
#             queryset = Resume.objects.all()
#             if region_values:
#                 queryset = queryset.filter(regions__region__icontains=region_values[0].strip())
                
#         return queryset.distinct()
    
# class PostKeywordSearchView(BaseSearchView):
#     serializer_class = PostSerializer
    
#     def get_queryset(self):
#         region_param=self.request.GET.get('region','')
        
#         region_value = region_param if region_param else []
        
#         region_query = Q()
#         for word in region_value:
#             region_query |= Q(region__contains=word.strip())
            
#         queryset = Post.objects.all()
        
#         if region_query:
#             queryset = queryset.filter(region_query)
            
#         return queryset.distinct()