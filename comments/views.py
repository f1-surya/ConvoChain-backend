from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView

from meta.models import Meta
from retweets.serializers import ReTweetSerializer
from tweets.serializers import TweetSerializer
from .models import Comment
from .serializers import CommentSerializer


class CommentView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        parent = Meta.objects.get(pk=pk)
        meta = Meta.objects.create(author=request.user, content_type='comment')
        Comment.objects.create(meta=meta, parent=parent, body=request.data['body'])

        return Response(HTTP_201_CREATED)

    def get(self, request, pk):
        meta = Meta.objects.get(pk=pk)
        comments = Comment.objects.filter(parent=meta)
        comments = sorted(comments, key=lambda comment: comment.meta.posted_date, reverse=True)
        serializer = CommentSerializer(data=comments, many=True, context={'user': request.user})
        serializer.is_valid()

        thread = []
        while True:
            if meta.content_type == 'tweet':
                tweet_serializer = TweetSerializer(instance=meta.tweet,
                                                   context={'user': request.user, 'comments': False})
                thread.append(tweet_serializer.data)
                break
            elif meta.content_type == 'retweet':
                retweet_serializer = ReTweetSerializer(instance=meta.retweet,
                                                       context={'user': request.user, 'comments': False})
                thread.append(retweet_serializer.data)
                break
            comment_serializer = CommentSerializer(instance=meta.comment, context={'user': request.user})
            thread.append(comment_serializer.data)
            meta = meta.comment.parent

        thread.sort(key=lambda content: content['meta']['posted_date'])

        return Response([thread, serializer.data])
