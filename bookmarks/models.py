from django.db import models
from accounts.models import User
from post.models import Post
from consumer.models import Resume
from community.models import Board


# Create your models here.

#Post
class Postbookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'post'),)

    def __str__(self):
        return f'{self.user.name}님이 즐겨찾기 추가한 {self.post.title}'

#Resume
class Resumebookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'resume'),)

    def __str__(self):
        return f'{self.user.name}님이 즐겨찾기 추가한 {self.resume.title}'


#Board
class Boardbookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'board'),)

    def __str__(self):
        return f'{self.user.name}님이 즐겨찾기 추가한 {self.board.title}'

