from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView

from meta.models import Meta
from retweets.models import ReTweet


class ReTweets(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        content_meta = Meta.objects.get(pk=request.data['pk'])
        if content_meta.content_type == 'retweet':
            return Response(data='You cannot retweet Retweets for now')

        meta = Meta.objects.create(author=request.user, content_type='retweet')
        ReTweet.objects.create(content=content_meta, meta=meta)
        return Response(HTTP_201_CREATED)

    def delete(self, request):
        content = Meta.objects.get(pk=request.GET.get('pk'))
        ReTweet.objects.get(content=content).meta.delete()
        return Response(data={'message': 'Reversed Retweet'})
