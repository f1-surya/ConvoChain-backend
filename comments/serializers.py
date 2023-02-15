from rest_framework.fields import SerializerMethodField, CharField
from rest_framework.serializers import ModelSerializer

from .models import Comment


class CommentSerializer(ModelSerializer):
    liked_by_user = SerializerMethodField('get_liked_by_user')
    author = CharField(source='author.username', read_only=True)
    author_name = SerializerMethodField('get_author_name')

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('body', 'author', 'posted_date', 'liked_by_user', 'tweet')

    def get_liked_by_user(self, comment):
        user = self.context['user']
        return comment.likes.filter(id=user.id).exists()

    def get_tweet(self, comment):
        tweet = self.context['tweet']
        return tweet

    def get_author_name(self, comment):
        user = comment.author
        return user.first_name + ' ' + user.last_name

