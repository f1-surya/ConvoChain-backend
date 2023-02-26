from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from meta.serializers import MetaSerializer
from retweets.models import ReTweet


class ReTweetSerializer(ModelSerializer):
    meta = SerializerMethodField('get_meta')

    class Meta:
        model = ReTweet
        fields = '__all__'

    def get_meta(self, retweet):
        meta = retweet.meta
        serializer = MetaSerializer(instance=meta, context=self.context)
        return serializer.data
