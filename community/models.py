from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage as storage


class Board(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(default="")
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    image1 = models.FileField(upload_to="image/%Y/%m/%d/", null=True, blank=True)
    image2 = models.FileField(upload_to="image/%Y/%m/%d/", null=True, blank=True)
    image3 = models.FileField(upload_to="image/%Y/%m/%d/", null=True, blank=True)
    image4 = models.FileField(upload_to="image/%Y/%m/%d/", null=True, blank=True)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="liked_boards"
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.pk:
            original_board = Board.objects.get(pk=self.pk)
            if original_board.image1.name != self.image1.name:
                storage.delete(original_board.image1.name)
            if original_board.image2.name != self.image2.name:
                storage.delete(original_board.image2.name)
            if original_board.image3.name != self.image3.name:
                storage.delete(original_board.image3.name)
            if original_board.image4.name != self.image4.name:
                storage.delete(original_board.image4.name)

        super().save(*args, **kwargs)

    @property
    def like_count(self):
        return self.likes.count()


class Comment(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="comments")
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on {self.board.title}"
