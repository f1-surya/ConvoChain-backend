from rest_framework.fields import SerializerMethodField, CharField
from rest_framework.serializers import ModelSerializer

from comments.models import Comment
from meta.models import Meta
from retweets.models import ReTweet


class MetaSerializer(ModelSerializer):
    author = CharField(source='author.username', read_only=True)
    author_name = SerializerMethodField('get_author_name')
    liked_by_user = SerializerMethodField('get_liked_by_user')
    comment_count = SerializerMethodField('get_comment_count')
    retweet_count = SerializerMethodField('get_retweet_count')
    retweeted_by_user = SerializerMethodField('get_retweeted_by_user')

    class Meta:
        model = Meta
        exclude = ('likes',)

    def get_author_name(self, meta):
        user = meta.author
        return user.first_name + ' ' + user.last_name

    def get_liked_by_user(self, meta):
        user = self.context['user']
        return meta.likes.filter(id=user.id).exists()

    def get_comment_count(self, meta):
        comments = Comment.objects.filter(parent=meta)
        return len(comments)

    def get_retweet_count(self, meta):
        retweets = ReTweet.objects.filter(content=meta)
        return len(retweets)

    def get_retweeted_by_user(self, meta):
        return ReTweet.objects.filter(content=meta).filter(meta__author=self.context['user']).exists()
