from itertools import chain

from django.db.models import F
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

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
                metas = chain(metas, Meta.objects.filter(author=follow.user))

        tweets = []
        retweets = []
        for meta in metas:
            if meta.content_type == 'tweet':
                tweets.append(meta.tweet)
            elif meta.content_type == 'retweet':
                retweets.append(meta.retweet)

        tweet_serializer = TweetSerializer(data=tweets, many=True, context={'user': request.user, 'comments': True})
        tweet_serializer.is_valid()

        retweet_serializer = ReTweetSerializer(data=retweets, many=True,
                                               context={'user': request.user, 'comments': True})
        retweet_serializer.is_valid()

        data = chain(tweet_serializer.data, retweet_serializer.data)
        data = sorted(data, key=lambda content: content['meta']['posted_date'], reverse=True)
        return Response(data)

    def put(self, request):
        meta = Meta.objects.get(pk=request.data['pk'])
        if meta.likes.filter(id=request.user.id).exists():
            meta.likes.remove(request.user)
            meta.likes_count = F('likes_count') - 1
        else:
            meta.likes.add(request.user)
            meta.likes_count = F('likes_count') + 1

        meta.save()

        return Response(HTTP_200_OK)
