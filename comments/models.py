from django.contrib.auth.models import User
from django.db.models import Model, ForeignKey, CharField, IntegerField, ManyToManyField, DateTimeField, CASCADE

from tweets.models import Tweet


class Comment(Model):
    author = ForeignKey(User, on_delete=CASCADE)
    body = CharField(max_length=255)
    likes_count = IntegerField(default=0)
    tweet = ForeignKey(Tweet, on_delete=CASCADE)
    comments = ManyToManyField('self', blank=True)
    posted_date = DateTimeField(auto_now_add=True)
    likes = ManyToManyField(User, blank=True, related_name='comment_likes')

    def __str__(self):
        return self.body
