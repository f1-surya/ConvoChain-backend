from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Tweet, Comment


class NewUserForm(UserCreationForm):
    email = forms.EmailField(label='email')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


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
