from django.contrib.auth.models import User
from django.db import models

from tweets.models import Tweet


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    likes_count = models.IntegerField(default=0)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    comments = models.ManyToManyField('self', blank=True)
    posted_date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name='comment_likes')

    def __str__(self):
        return self.comment
