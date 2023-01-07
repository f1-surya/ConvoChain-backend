from rest_framework import serializers

from userManagement.serializers import ProfileSerializer
from .models import Tweet, Comment


class TweetSerializer(serializers.ModelSerializer):
    posted_by = ProfileSerializer(many=False)
    liked_by_user = serializers.SerializerMethodField('get_liked_by_user')

    class Meta:
        model = Tweet
        fields = ('id', 'tweet', 'posted_by', 'posted_date', 'likes_count', 'liked_by_user')
        read_only_fields = ('id', 'tweet', 'posted_by', 'posted_date', 'liked_by_user')

    def get_liked_by_user(self, tweet):
        user = self.context['user']
        if user.is_authenticated:
            likes = tweet.likes.all()
            for like in likes:
                if like.get(tweet).contains(user):
                    return True
                elif like == user:
                    return True

            return False


class CommentSerializer(serializers.ModelSerializer):
    liked_by_user = serializers.SerializerMethodField('get_liked_by_user')

    class Meta:
        model = Comment
        fields = ('id', 'comment', 'posted_by', 'posted_date', 'likes_count', 'liked_by_user')
        read_only_fields = ('comment', 'posted_by', 'posted_date', 'liked_by_user')

    def get_liked_by_user(self, comment):
        user = self.context['user']
        if user.is_authenticated:
            likes = comment.likes.all()
            for like in likes:
                if like.get(comment).contains(user):
                    return True
                elif like == user:
                    return True

            return False
