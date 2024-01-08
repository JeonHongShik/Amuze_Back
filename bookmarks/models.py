from django.conf import settings
from django.db import models
from post.models import Post
from consumer.models import Resume
from community.models import Board


# Create your models here.

#Post
class Postbookmark(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('author', 'post'),)

    def __str__(self):
        return f'{self.author.displayName}님이 즐겨찾기 추가한 {self.post.title}'


#Resume
class Resumebookmark(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('author', 'resume'),)

    def __str__(self):
        return f'{self.author.displayName}님이 즐겨찾기 추가한 {self.resume.title}'


#Board
class Boardbookmark(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('author', 'board'),)

    def __str__(self):
        return f'{self.author.displayName}님이 즐겨찾기 추가한 {self.board.title}'

