from django.db import models
from accounts.models import User
from post.models import Post

# Create your models here.
class bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'post'),)

    def __str__(self):
        return f'{self.user.name}님이 즐겨찾기 추가한 {self.post.title}'
