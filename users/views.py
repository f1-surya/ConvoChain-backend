from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db.models import F
from knox.auth import TokenAuthentication
from knox.views import LoginView as KnoxLoginView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from tweets.models import Tweet
from tweets.serializers import TweetSerializer
from users.models import UserProfile
from users.serializers import RegisterSerializer, ProfileSerializer


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class LoginView(KnoxLoginView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)


class ProfileView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = User.objects.get(username=request.data['username'])
        user_profile = UserProfile.objects.get(user=user)
        profile_serializer = ProfileSerializer(data=user_profile)

        if request.data['query'] == 'likes':
            likes = Tweet.objects.filter(likes=user.id)
            tweets_serializer = TweetSerializer(data=likes, many=True, context={'user': user})
            tweets_serializer.is_valid()
            return Response({'profile': profile_serializer.data,
                             'likes': tweets_serializer.data}, HTTP_200_OK)

        if request.data['query'] == 'followers':
            followers = UserProfile.objects.filter(follows=user_profile)
            followers_serializer = ProfileSerializer(data=followers, many=True)
            followers_serializer.is_valid()
            return Response(followers_serializer.data)

        if request.data['query'] == 'following':
            following = user_profile.follows
            follows_serializer = ProfileSerializer(data=following, many=True)
            follows_serializer.is_valid()
            return Response(follows_serializer.data)

        tweets = Tweet.objects.filter(author=user)
        tweets_serializer = TweetSerializer(data=tweets, many=True, context={'user': user})
        tweets_serializer.is_valid()
        return Response({'profile': profile_serializer.data,
                         'tweets': tweets_serializer.data})

    def put(self, request, pk=None):
        user_profile = UserProfile.objects.get(user=request.user)

        if request.data['query'] == 'follow':
            user_to_follow = User.objects.get(username=request.data['username'])
            profile_to_follow = UserProfile.objects.get(user=user_to_follow)

            if user_profile.follows.filter(follows=profile_to_follow).exists():
                user_profile.follows.remove(profile_to_follow)
                user_profile.following_count = F('following_count') - 1
                profile_to_follow.followers_count = F('followers_count') - 1
            else:
                user_profile.follows.add(profile_to_follow)
                user_profile.following_count = F('following_count') + 1
                profile_to_follow.followers_count = F('followers_count') + 1

            user_profile.save()
            profile_to_follow.save()

        user_profile.about = request.data['about']
        user_profile.save()

        return Response()
