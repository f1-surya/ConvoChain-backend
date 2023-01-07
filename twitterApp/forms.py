from django import forms

from .models import Tweet, Comment


class NewTweetForm(forms.Form):
    body = forms.CharField(required=True)

    class Meta:
        model = Tweet
        exclude = ('user', )


class NewCommentForm(forms.Form):
    body = forms.CharField(required=True)

    class Meta:
        model = Comment
        exclude = ('user', )
