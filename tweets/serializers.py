from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer, CharField

from .models import Tweet


class TweetSerializer(ModelSerializer):
    liked_by_user = SerializerMethodField('get_liked_by_user')
    author = CharField(source='author.username', read_only=True)

    class Meta:
        model = Tweet
        fields = '__all__'
        read_only_fields = ['author']

    def get_liked_by_user(self, tweet):
        user = self.context['user']
        likes = tweet.likes.all()
        for like in likes:
            if like == user:
                return True

        return False
