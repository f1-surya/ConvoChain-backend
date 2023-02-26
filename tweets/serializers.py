from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from meta.serializers import MetaSerializer
from .models import Tweet


class TweetSerializer(ModelSerializer):
    meta = SerializerMethodField('get_meta')

    class Meta:
        model = Tweet
        fields = '__all__'

    def get_meta(self, tweet):
        meta = tweet.meta
        serializer = MetaSerializer(instance=meta, context=self.context)
        return serializer.data
