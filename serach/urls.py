from django.urls import path
from .views import BoardSearchView,PostSearchView,ResumeSearchView


urlpatterns = [
    path('boardsearch/', BoardSearchView.as_view(), name='boardsearch'),
    path('postsearch/', PostSearchView.as_view(), name='postsearch'),
    path('resumesearch/', ResumeSearchView.as_view(), name='resumesearch'),

]
