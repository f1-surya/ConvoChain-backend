from django.contrib.auth.models import User
from django.db import models
from django.db.models import ForeignKey, CharField, IntegerField, DateTimeField, ManyToManyField, Model


class Tweet(Model):
    author = ForeignKey(User, on_delete=models.DO_NOTHING)
    body = CharField(max_length=255)
    likes_count = IntegerField(default=0)
    posted_date = DateTimeField('posted date', auto_now_add=True)
    likes = ManyToManyField(User, blank=True, related_name='likes')

    def __str__(self):
        return self.body

    def get_author(self):
        return self.author
