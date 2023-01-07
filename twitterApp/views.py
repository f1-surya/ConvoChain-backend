from itertools import chain
from operator import attrgetter

from django.db.models import F
from django.http import JsonResponse, HttpResponseRedirect
from rest_framework import viewsets

from .forms import NewTweetForm, NewCommentForm
from .models import Tweet, UserProfile, Comment
from .serializers import TweetSerializer, ProfileSerializer, CommentSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()

    def get_serializer_class(self):
        return ProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.get(pk=self.request.pk)


class ProfilesViewsSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        return ProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.exclude(self.request.user)


def get_tweets(request):
    if request.user.is_authenticated:
        follows = request.user.userprofile.follows.all()
        tweets = []
        for followed in follows:
            if len(tweets) == 0:
                tweets.append(Tweet.objects.filter(posted_by=followed.user))
            else:
                followed_tweets = Tweet.objects.filter(posted_by=followed.user)
                tweets = sorted(chain(tweets[-1], followed_tweets), key=attrgetter('posted_date'))

        serializer = TweetSerializer(tweets, many=True, context={'user': request.user})
        return JsonResponse(serializer.data, safe=False)


def tweet(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = NewTweetForm(request.POST)
            if form.is_valid():
                new_tweet = Tweet()
                new_tweet.tweet = form.cleaned_data['body']
                new_tweet.posted_by = request.user
                new_tweet.save()
                return JsonResponse(data={'message': 'Tweet saved'})
        else:
            return HttpResponseRedirect('/login')

    return JsonResponse(data={})


def like(request, pk):
    if request.method == 'POST' and request.user.is_authenticated:
        tweet_instance = Tweet.objects.get(pk=pk)
        if tweet_instance.likes.filter(id=request.user.id).exists():
            tweet_instance.likes.remove(request.user)
            tweet_instance.likes_count = F('likes_count') - 1
        else:
            tweet_instance.likes_count = F('likes_count') + 1
            tweet_instance.likes.add(request.user)

        tweet_instance.save()

    return JsonResponse({})


def add_comment(request, pk):
    if request.method == 'POST' and request.user.is_authenticated:
        form = NewCommentForm(request.POST)
        tweet_instance = Tweet.objects.get(pk=pk)
        if form.is_valid():
            new_comment = Comment()
            new_comment.comment = form.cleaned_data['body']
            new_comment.posted_by = request.user
            new_comment.tweet = tweet_instance
            new_comment.save()

    return JsonResponse({})


def get_comments(request, pk):
    if request.user.is_authenticated:
        tweet_instance = Tweet.objects.get(pk=pk)
        comments = Comment.objects.filter(tweet=tweet_instance)
        serializer = CommentSerializer(comments, many=True, context={'user': request.user})
        return JsonResponse(serializer.data, safe=False)


def like_comment(request, pk):
    if request.method == 'POST' and request.user.is_authenticated:
        comment_instance = Comment.objects.get(pk=pk)
        if comment_instance.likes.filter(id=request.user.id).exists():
            comment_instance.likes.remove(request.user)
            comment_instance.likes_count = F('likes_count') - 1
        else:
            comment_instance.likes_count = F('likes_count') + 1
            comment_instance.likes.add(request.user)

        comment_instance.save()

    return JsonResponse({})
