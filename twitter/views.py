from itertools import chain

from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from comments.serializers import CommentSerializer
from meta.models import Meta
from retweets.serializers import ReTweetSerializer
from tweets.serializers import TweetSerializer


class GetData(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        follows = request.user.userprofile.follows.all()
        metas = None
        for follow in follows:
            if metas is None:
                metas = Meta.objects.filter(author=follow.user)
            else:
                followed_metas = Meta.objects.filter(author=follow.user)
                metas = chain(metas, followed_metas)

        tweets = []
        comments = []
        retweets = []
        for meta in metas:
            if meta.content_type == 'tweet':
                tweets.append(meta.tweet)
            elif meta.content_type == 'retweet':
                retweets.append(meta.retweet)
            elif meta.content_type == 'comment':
                comments.append(meta.comment)

        tweet_serializer = TweetSerializer(data=tweets, many=True, context={'user': request.user})
        tweet_serializer.is_valid()

        comment_serializer = CommentSerializer(data=comments, many=True, context={'user': request.user})
        comment_serializer.is_valid()

        retweet_serializer = ReTweetSerializer(data=retweets, many=True, context={'user': request.user})
        retweet_serializer.is_valid()

        data = chain(tweet_serializer.data, comment_serializer.data, retweet_serializer.data)
        data = sorted(data, key=lambda content: content['meta']['posted_date'], reverse=True)
        return Response(data)