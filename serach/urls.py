from django.urls import path
from .views import BoardSearchView,PostSearchView,ResumeSearchView
from .views import PostKeywordSearchView,ResumeKeywordSearchView

urlpatterns = [
    path('boardsearch/', BoardSearchView.as_view(), name='boardsearch'),
    path('postsearch/', PostSearchView.as_view(), name='postsearch'),
    path('resumesearch/', ResumeSearchView.as_view(), name='resumesearch'),
    path('keywordpostsearch/', PostKeywordSearchView.as_view(), name='postkeywordserach'),
    path('keywordresumesearch/', ResumeKeywordSearchView.as_view(), name='resumekeywordserach'),
]
