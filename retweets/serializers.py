from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from comments.serializers import CommentSerializer
from meta.serializers import MetaSerializer
from retweets.models import ReTweet
from tweets.serializers import TweetSerializer


class ReTweetSerializer(ModelSerializer):
    meta = SerializerMethodField('get_meta')
    content = SerializerMethodField('get_content')

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
            serializer = TweetSerializer(instance=content.tweet, context=self.context)
            return serializer.data

        elif content.content_type == 'comment':
            serializer = CommentSerializer(instance=content.comment, context=self.context)
            return serializer.data
