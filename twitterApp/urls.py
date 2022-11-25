from django.urls import path
from .views import *

urlpatterns = [
    path('', get_tweets, name='get_tweets'),
    path('register', register, name='register'),
    path('login', user_login, name='login'),
    path('logout', user_logout, name='logout'),
    path('profile_list', ProfilesViewsSet.as_view, name='profile_list'),
    path('profile/<int:pk>', ProfileViewSet.as_view, name='profile'),
    path('tweet', tweet, name='tweet'),
    path('like/<int:pk>', like, name='like'),
    path('comments/<int:pk>', get_comments, name='comments'),
    path('comment/<int:pk>', add_comment, name='add_comment'),
    path('like-comment/<int:pk>', like_comment, name='like_comment')
]
