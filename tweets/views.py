from itertools import chain
from operator import attrgetter

from django.db.models import F
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK
from rest_framework.views import APIView

from .models import Tweet
from .serializers import TweetSerializer


class Tweets(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = TweetSerializer(data=request.data, context={'user': request.user})

        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            print(serializer.errors)

        return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        follows = request.user.userprofile.follows.all()
        tweets = None
        for followed in follows:
            if tweets is None:
                tweets = Tweet.objects.filter(author=followed.user)
            else:
                followed_tweets = Tweet.objects.filter(author=followed.user)
                tweets = sorted(chain(tweets, followed_tweets), key=attrgetter('posted_date'), reverse=True)

        serializer = TweetSerializer(data=tweets, many=True, context={'user': request.user})
        serializer.is_valid()
        return Response(serializer.data, HTTP_200_OK)

    def put(self, request):
        tweet_instance = Tweet.objects.get(pk=request.data['pk'])
        if tweet_instance.likes.filter(id=request.user.id).exists():
            tweet_instance.likes.remove(request.user)
            tweet_instance.likes_count = F('likes_count') - 1
        else:
            tweet_instance.likes.add(request.user)
            tweet_instance.likes_count = F('likes_count') + 1

        tweet_instance.save()

        return Response(HTTP_200_OK)
