from django.db.models import F
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.views import APIView

from meta.models import Meta
from .models import Tweet


class Tweets(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        meta = Meta.objects.create(author=request.user, content_type='tweet')
        Tweet.objects.create(meta=meta, body=request.data['body'])
        return Response(HTTP_201_CREATED)

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
