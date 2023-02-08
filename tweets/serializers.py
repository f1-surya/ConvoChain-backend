from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer, CharField

from comments.models import Comment
from .models import Tweet


class TweetSerializer(ModelSerializer):
    author = CharField(source='author.username', read_only=True)
    author_name = SerializerMethodField('get_author_name')
    liked_by_user = SerializerMethodField('get_liked_by_user')
    comment_count = SerializerMethodField('get_comment_count')

    class Meta:
        model = Tweet
        exclude = ('likes',)

    def get_liked_by_user(self, tweet):
        user = self.context['user']
        if tweet.likes.filter(id=user.id).exists():
            return True

        return False

    def get_comment_count(self, tweet):
        comments = Comment.objects.filter(tweet=tweet)
        return len(comments)

    def get_author_name(self, tweet):
        user = tweet.author
        return user.first_name + ' ' + user.last_name
