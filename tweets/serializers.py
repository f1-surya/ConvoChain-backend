from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer, CharField

from comments.models import Comment
from .models import Tweet


class TweetSerializer(ModelSerializer):
    liked_by_user = SerializerMethodField('get_liked_by_user')
    author = CharField(source='author.username', read_only=True)
    comment_count = SerializerMethodField('get_comment_count')

    class Meta:
        model = Tweet
        fields = '__all__'
        read_only_fields = ('body', 'author', 'posted_date', 'liked_by_user')

    def get_liked_by_user(self, tweet):
        user = self.context['user']
        likes = tweet.likes.all()
        for like in likes:
            if like == user:
                return True

        return False

    def get_comment_count(self, tweet):
        comments = Comment.objects.filter(tweet=tweet)
        return len(comments)
