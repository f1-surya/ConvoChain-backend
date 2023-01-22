from django.contrib.auth.models import User
from django.db import models


class Tweet(models.Model):
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    body = models.CharField(max_length=255)
    likes_count = models.IntegerField(default=0)
    posted_date = models.DateTimeField('posted date', auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')

    def __str__(self):
        return self.body

    def get_author(self):
        return self.author
