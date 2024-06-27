from itertools import chain

from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from comments.models import Comment
from comments.serializers import CommentSerializer
from meta.serializers import MetaSerializer
from .models import Tweet


class TweetSerializer(ModelSerializer):
    meta = SerializerMethodField('get_meta')
    comments = SerializerMethodField('get_comments')

    class Meta:
        model = Tweet
        fields = '__all__'

    def get_meta(self, tweet):
        meta = tweet.meta
        serializer = MetaSerializer(instance=meta, context=self.context)
        return serializer.data

    def get_comments(self, tweet):
        if not self.context['comments']:
            return []

        follows = self.context['user'].userprofile.follows.all()
        comments = Comment.objects.filter(parent=tweet.meta)
        comments_list = None
        for follow in follows:
            if comments_list is None:
                comments_list = comments.filter(meta__author=follow.user)
            else:
                comments_list = chain(comments_list, comments.filter(meta__author=follow.user))

        comments_list = sorted(comments_list, key=lambda comment: comment.meta.posted_date, reverse=True)
        serializer = CommentSerializer(instance=comments_list, context=self.context, many=True)
        return serializer.data
