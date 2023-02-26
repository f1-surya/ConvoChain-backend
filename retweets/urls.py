from django.urls import path
from .views import *

urlpatterns = [
    path('retweet', ReTweets.as_view(), name='get_retweets'),
]
