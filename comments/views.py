from django.db.models import F
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
from rest_framework.views import APIView

from tweets.models import Tweet
from .models import Comment
from .serializers import CommentSerializer


class CommentView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        tweet = Tweet.objects.get(pk=pk)
        comment = Comment()
        comment.body = request.data['body']
        comment.author = request.user
        comment.tweet = tweet
        comment.save()

        return Response(HTTP_201_CREATED)

    def get(self, request, pk):
        tweet = Tweet.objects.get(pk=pk)
        comments = Comment.objects.filter(tweet=tweet)
        serializer = CommentSerializer(data=comments, many=True, context={'user': request.user})
        serializer.is_valid()

        return Response(serializer.data, HTTP_200_OK)

    def put(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        if comment.likes.filter(id=request.user.id).exists():
            comment.likes.remove(request.user)
            comment.likes_count = F('likes_count') - 1
        else:
            comment.likes.add(request.user)
            comment.likes_count = F('likes_count') + 1

        comment.save()

        return Response(HTTP_200_OK)
