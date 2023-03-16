from itertools import chain

from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from comments.models import Comment
from comments.serializers import CommentSerializer
from meta.serializers import MetaSerializer
from retweets.models import ReTweet
from tweets.serializers import TweetSerializer


class ReTweetSerializer(ModelSerializer):
    meta = SerializerMethodField('get_meta')
    content = SerializerMethodField('get_content')
    comments = SerializerMethodField('get_comments')

    class Meta:
        model = ReTweet
        fields = '__all__'

    def get_meta(self, retweet):
        meta = retweet.meta
        serializer = MetaSerializer(instance=meta, context=self.context)
        return serializer.data

    def get_content(self, retweet):
        content = retweet.content
        if content.content_type == 'tweet':
            serializer = TweetSerializer(instance=content.tweet, context={'user': self.context['user'], 'comments': False})
            return serializer.data

        elif content.content_type == 'comment':
            serializer = CommentSerializer(instance=content.comment, context=self.context)
            return serializer.data

    def get_comments(self, retweet):
        if not self.context['comments']:
            return []
        follows = self.context['user'].userprofile.follows.all()
        comments = Comment.objects.filter(parent=retweet.meta)
        comments_list = None
        for follow in follows:
            if comments_list is None:
                comments_list = comments.filter(meta__author=follow.user)
            else:
                comments_list = chain(comments_list, comments.filter(meta__author=follow.user))

        serializer = CommentSerializer(instance=comments_list, context=self.context, many=True)
        return serializer.data
