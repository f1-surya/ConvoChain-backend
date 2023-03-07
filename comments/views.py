from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
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
        if meta.content_type == 'tweet':
            parent_serializer = TweetSerializer(instance=meta.tweet, context={'user': request.user})
        elif meta.content_type == 'comment':
            parent_serializer = CommentSerializer(instance=meta.comment, context={'user': request.user})
        else:
            parent_serializer = ReTweetSerializer(instance=meta.retweet, context={'user': request.user})

        comments = Comment.objects.filter(parent=meta)
        serializer = CommentSerializer(data=comments, many=True, context={'user': request.user})
        serializer.is_valid()

        return Response([parent_serializer.data, serializer.data], HTTP_200_OK)
