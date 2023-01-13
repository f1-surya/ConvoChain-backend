from django.urls import path
from .views import *

urlpatterns = [
    path('', Tweets.as_view(), name='get_tweets'),
]
