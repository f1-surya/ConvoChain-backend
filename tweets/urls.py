from django.urls import path
from .views import *

urlpatterns = [
    path('tweets', Tweets.as_view(), name='tweets'),
]
