from django import forms
from .models import Board, Comment, Reply


class BoardForm(forms.ModelForm):
    title = forms.CharField(
        error_messages={"required": "제목을 입력하세요"},
        label="제목",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    content = forms.CharField(
        error_messages={"required": "내용을 입력하세요"},
        label="내용",
        widget=forms.Textarea(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Board
        fields = ("title", "content")


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        error_messages={"required": "댓글을 입력하세요"},
        label="댓글",
        widget=forms.Textarea(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Comment
        fields = ("content",)


class ReplyForm(forms.ModelForm):
    content = forms.CharField(
        error_messages={"required": "답글을 입력하세요"},
        label="답글",
        widget=forms.Textarea(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Reply
        fields = ("content",)
