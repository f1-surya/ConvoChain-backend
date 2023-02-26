from django.db.models import F
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
from rest_framework.views import APIView

from meta.models import Meta
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
        serializer = CommentSerializer(data=comments, many=True, context={'user': request.user})
        serializer.is_valid()

        return Response(serializer.data, HTTP_200_OK)

    def put(self, request, pk):
        meta = Meta.objects.get(pk=pk)
        if meta.likes.filter(id=request.user.id).exists():
            meta.likes.remove(request.user)
            meta.likes_count = F('likes_count') - 1
        else:
            meta.likes.add(request.user)
            meta.likes_count = F('likes_count') + 1

        meta.save()

        return Response(HTTP_200_OK)
