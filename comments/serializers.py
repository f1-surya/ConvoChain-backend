from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from .models import Comment


class CommentSerializer(ModelSerializer):
    liked_by_user = SerializerMethodField('get_liked_by_user')

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('body', 'author', 'posted_date', 'liked_by_user', 'tweet')

    def get_liked_by_user(self, comment):
        user = self.context['user']
        likes = comment.likes.all()
        for like in likes:
            if like == user:
                return True

        return False

    def get_tweet(self, comment):
        tweet = self.context['tweet']
        print(tweet)
        return tweet
